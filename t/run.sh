#!/bin/sh
# Golden tests: run each t/NNN-name.smol, examples/name.smol and
# docs/guide/code/name.smol that has a .expected next to it (or the files
# given) through the interpreter, and diff what it prints against the
# .expected: stdout and stderr together, then "exit: N" if it exits with N
# other than 0.
# $JOBS tests run at once (default: one per CPU). Each says ok or FAIL as
# it finishes; what each failure printed comes at the end, in order.
cd "$(dirname "$0")/.." || exit 2
# A test that runs longer than $TIMEOUT seconds is killed, and fails.
# (macOS has no timeout(1), hence the watchdog.)
TIMEOUT=${TIMEOUT-60}
export TIMEOUT

# What every test assumes of the runtime: a virtual clock, a seed, a heap cap,
# as the runtime gains them. None exist yet, so nothing is set here.

# One test, run by xargs below: its status line, and what went wrong in
# build/t/$name.fail.
if [ "$1" = "--one" ]; then
    src=$2
    name=$(basename "$src")
    name=${name%.*}
    out=build/t/$name.out
    # The test runs in the foreground, under an alarm. A watchdog in the
    # background was killed when the test finished, and bash on macOS (where
    # /bin/sh is bash) reports every killed job as "Terminated". perl ships with
    # macOS and Linux, and its alarm survives exec: an alarm that goes off
    # ends the program with status 142, which is reported as a timeout.
    if command -v perl >/dev/null 2>&1; then
        perl -e 'alarm shift @ARGV; exec @ARGV or die "exec: $!\n"' "$TIMEOUT" node bin/smol.ts "$src" >"$out" 2>&1
    else
        node bin/smol.ts "$src" >"$out" 2>&1
    fi
    status=$?
    [ $status -eq 142 ] && echo "killed after ${TIMEOUT}s" >>"$out"
    [ $status -eq 0 ] || echo "exit: $status" >>"$out"
    if diff -u "${src%.*}.expected" "$out" >"build/t/$name.fail"; then
        rm -f "build/t/$name.fail"
        echo "ok   $name"
    else
        echo "FAIL $name"
        exit 1
    fi
    exit 0
fi

if [ $# -eq 0 ]; then
    set --
    for src in t/*.smol examples/*.smol docs/guide/code/*.smol; do
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
