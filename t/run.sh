#!/bin/sh
# Golden tests: compile each t/NNN-name.pl, examples/name.pl and
# docs/guide/code/name.pl that has a .expected next to it (or the files
# given), run it, and diff what it prints against the .expected: stdout
# and stderr together, then "exit: N" if it exits with N other than 0.
#
# A test's headers are comments before its first statement. "# kind:" is
# what the test is (t/README.md): same (the default), dies, fault and new
# are compiled and run; refused must NOT compile, and its .expected is
# what the compiler said and "exit: 1". "# stdin: bytes" is what the test
# reads from stdin, written with printf %b's escapes (\n, \t, \\, \0nnn
# in octal; \033 is ESC); without one, stdin is empty. "# args: words"
# gives the program its arguments, split at spaces, and
# "# env: NAME=value ..." sets variables for it.
#
# Whether a .expected is right is not this script's business: perl says,
# through t/checks.py oracle.
#
# $JOBS tests run at once (default: one per CPU). Each says ok or FAIL as
# it finishes; what each failure printed comes at the end, in order.
cd "$(dirname "$0")/.." || exit 2
# A test that runs longer than $TIMEOUT seconds is killed, and fails.
# (macOS has no timeout(1), hence the watchdog.)
TIMEOUT=${TIMEOUT-60}
export TIMEOUT
# And one that prints more than $OUTPUT_BLOCKS blocks of 512 bytes is
# stopped by the system (SIGXFSZ), and fails: a loop that prints without
# end fills a disk in the time the watchdog allows it (step 6). The
# largest test prints a hundredth of this.
OUTPUT_BLOCKS=${OUTPUT_BLOCKS-16384}
export OUTPUT_BLOCKS

# What every test assumes of the runtime. Add each knob as the runtime
# gains it, so that no test depends on the machine it runs on: the
# collector's stress interval, poison and heap cap (step 7, in
# t/knobs.sh), the virtual clock and the random seed (step 22).
. ./t/knobs.sh

# The value of one header, from the comments before the first statement.
header() {
    awk -v key="$1" '
        /^[ \t]*$/ { next }
        /^[ \t]*#/ { if (index($0, "# " key ": ") == 1) print substr($0, length(key) + 5); next }
        { exit }' "$2"
}

# The watchdog leaves a file to say it killed the test, since its own
# output can't go down the pipe to diff: diff would wait for it.
output() {
    rm -f "$1.killed" "$1.output"
    set -f                                  # $3 and $4 are split into words, not globbed
    # What it prints goes to a file, which is what the limit is on.
    ( ulimit -f "$OUTPUT_BLOCKS"; exec env $4 "./$1" $3 <"$2" >"$1.output" 2>&1 ) &
    set +f
    pid=$!
    ( sleep "$TIMEOUT" && : >"$1.killed" && kill "$pid" ) >/dev/null 2>&1 &
    watchdog=$!
    wait "$pid" 2>/dev/null
    status=$?
    kill "$watchdog" 2>/dev/null
    # A Mac's sh is bash 3.2, which says `Terminated: 15` of a job it finds
    # killed the next time it waits for a command, `cat` below being one.
    # Waiting for it here is where that is said, and it goes nowhere.
    wait "$watchdog" 2>/dev/null
    # 153 is 128 and SIGXFSZ: what it printed is not worth a diff.
    if [ $status -eq 153 ]; then
        echo "stopped: it printed more than $OUTPUT_BLOCKS blocks of 512 bytes"
    else
        cat "$1.output"
    fi
    rm -f "$1.output"
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
    kind=$(header kind "$src")
    case ${kind:-same} in
    refused)
        # The compiler's own exit status is the one that counts: 1 is a
        # refusal, and 2 is a compiler that broke, which is not one.
        node bin/curlyc.ts -o "$bin" "$src" >"$bin.out" 2>&1
        status=$?
        if [ $status -eq 0 ]; then
            echo "it compiled, and a refused test must not" >"$bin.fail"
        elif { cat "$bin.out"; echo "exit: $status"; } | diff -u "${src%.*}.expected" - >"$bin.fail"; then
            rm -f "$bin.fail"
            echo "ok   $name"
            exit 0
        fi
        echo "FAIL $name"
        exit 1 ;;
    same|dies|fault|new) ;;
    *)
        echo "unknown kind: $kind" >"$bin.fail"
        echo "FAIL $name"
        exit 1 ;;
    esac
    printf '%b' "$(header stdin "$src")" >"$bin.stdin"
    if ! node bin/curlyc.ts -o "$bin" "$src" >"$bin.fail" 2>&1; then
        echo "FAIL $name (compile)"
        exit 1
    elif output "$bin" "$bin.stdin" "$(header args "$src")" "$(header env "$src")" | diff -u "${src%.*}.expected" - >"$bin.fail"; then
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
    for src in t/*.pl examples/*.pl docs/guide/code/*.pl; do
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
