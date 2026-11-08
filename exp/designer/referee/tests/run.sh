#!/bin/sh
# Runs each tests/*.ditto through the referee and compares stdout+stderr
# (plus "exit: N" when N isn't 0) with the .expected file.
cd "$(dirname "$0")"
pass=0; fail=0
for f in *.ditto; do
  b=${f%.ditto}
  in=/dev/null; [ -f "$b.stdin" ] && in="$b.stdin"
  out=$(python3 ../referee.py "$f" <"$in" 2>&1; s=$?; [ $s -ne 0 ] && echo "exit: $s")
  if [ "$out" = "$(cat "$b.expected")" ]; then pass=$((pass+1)); else
    fail=$((fail+1)); echo "FAIL $f"; printf '%s\n' "$out" | diff "$b.expected" - ; fi
done
echo "$pass passed, $fail failed"
[ $fail -eq 0 ]
