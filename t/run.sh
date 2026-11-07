#!/bin/sh
# t/run.sh FILE.strata: build, run, diff against FILE.expected (stdout and
# stderr together, plus "exit: N" when N isn't 0). Silent when it passes.
root=$(cd "$(dirname "$0")/.." && pwd)
src=$1
name=$(basename "$src" .strata)
dir="$root/build/t"
mkdir -p "$dir"
actual="$dir/$name.actual"

if "$root/bin/strata" build "$src" -o "$dir/$name" 2>"$actual"; then
  "$dir/$name" >"$actual" 2>&1
  rc=$?
else
  rc=$?
  [ $rc -eq 2 ] || { echo "FAIL $src: bin/strata exited $rc" >&2; cat "$actual" >&2; exit 1; }
fi
if [ $rc -ne 0 ]; then
  # "exit: N" goes on a line of its own.
  [ -n "$(tail -c1 "$actual")" ] && echo >>"$actual"
  echo "exit: $rc" >>"$actual"
fi
if ! diff -u "${src%.strata}.expected" "$actual" >"$dir/$name.diff"; then
  echo "FAIL $src" >&2
  cat "$dir/$name.diff" >&2
  exit 1
fi
