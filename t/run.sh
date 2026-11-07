#!/bin/sh
# Golden tests: run each t/NNN-name.lang, examples/name.lang and
# docs/guide/code/name.lang that has a .expected next to it (or the files
# given) through the interpreter, `$LANG_NODE bin/lang.ts FILE`, and diff
# what it prints against the .expected: stdout and stderr together, then
# "exit: N" if it exits with N other than 0. $LANG_NODE is node unless
# set: `make golden-node` runs the suite under a second Node, the
# interpreter's second oracle (docs/PROCESS.md, "An interpreter").
# A line "; stdin: bytes" is what the test reads from stdin, written with
# printf %b's escapes (\n, \t, \\, \0nnn in octal; \033 is ESC); without
# one, stdin is empty. "; args: words" gives the program its arguments,
# split at spaces, and "; env: NAME=value ..." sets variables for it.
# $JOBS tests run at once (default: one per CPU). Each says ok or FAIL as
# it finishes; what each failure printed comes at the end, in order.
cd "$(dirname "$0")/.." || exit 2
# A test that runs longer than $TIMEOUT seconds is killed, and fails.
# (macOS has no timeout(1), hence the watchdog.)
TIMEOUT=${TIMEOUT-60}
LANG_NODE=${LANG_NODE-node}
export TIMEOUT LANG_NODE

# What every test assumes of the interpreter. Add each knob here as it
# gains one, so that no test depends on the machine it runs on:
# the virtual clock, the random seed, the epoch, the heap cap, the
# collector's poison. (None exist at step 0.)
# export LANG_CLOCK=virtual
# export LANG_SEED=1

# The watchdog leaves a file to say it killed the test, since its own
# output can't go down the pipe to diff: diff would wait for it.
# $1 is where the test's files go (build/t/NAME), $2 its stdin, $3 its
# arguments, $4 its environment, $5 the program.
output() {
    rm -f "$1.killed"
    set -f                                  # $3 and $4 are split into words, not globbed
    env $4 "$LANG_NODE" bin/lang.ts "$5" $3 <"$2" 2>&1 &
    set +f
    pid=$!
    ( sleep "$TIMEOUT" && : >"$1.killed" && kill "$pid" ) >/dev/null 2>&1 &
    watchdog=$!
    wait "$pid" 2>/dev/null
    status=$?
    kill "$watchdog" 2>/dev/null
    [ -f "$1.killed" ] && echo "killed after ${TIMEOUT}s"
    [ $status -eq 0 ] || echo "exit: $status"
}

# One test, run by xargs below: its status line, and what went wrong in
# $bin.fail.
if [ "$1" = "--one" ]; then
    src=$2
    name=$(basename "$src")
    name=${name%.*}
    bin=build/t/$name
    printf '%b' "$(sed -n 's#^; stdin: ##p' "$src")" >"$bin.stdin"
    if output "$bin" "$bin.stdin" "$(sed -n 's#^; args: ##p' "$src")" "$(sed -n 's#^; env: ##p' "$src")" "$src" | diff -u "${src%.*}.expected" - >"$bin.fail"; then
        rm -f "$bin.fail"
        echo "ok   $name"
    else
        echo "FAIL $name"
        exit 1
    fi
    exit 0
fi

if [ $# -eq 0 ]; then
    set --
    for src in t/*.lang examples/*.lang docs/guide/code/*.lang; do
        [ -f "${src%.*}.expected" ] && set -- "$@" "$src"
    done
fi
mkdir -p build/t
JOBS=${JOBS-$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 1)}

for src in "$@"; do
    name=$(basename "$src")
    rm -f "build/t/${name%.*}.fail"
done
printf '%s\n' "$@" | xargs -n 1 -P "$JOBS" ./t/run.sh --one

fail=0
for src in "$@"; do
    name=$(basename "$src")
    name=${name%.*}
    if [ -f "build/t/$name.fail" ]; then
        [ $fail -eq 0 ] && echo
        echo "--- $name"
        cat "build/t/$name.fail"
        fail=$((fail + 1))
    fi
done
echo "$# tests, $fail failed"
[ $fail -eq 0 ]
