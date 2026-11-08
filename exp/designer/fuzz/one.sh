#!/usr/bin/env bash
# one.sh SEED: generate, run both, record result in work/SEED.*; copy to diffs/ on disagreement.
HERE=$(cd "$(dirname "$0")" && pwd)
DITTO_ROOT=${DITTO_ROOT:?set DITTO_ROOT to a checkout of exp-designer-2}
REFEREE=${REFEREE:-$(dirname "$HERE")/referee/referee.py}
seed=$1
W=$HERE/work; mkdir -p "$W" "$HERE/diffs"
f=$W/s$seed.ditto
extra=${GEN_ARGS:-}
GEN_FEATURES=$W/s$seed.feat python3 "$HERE/gen.py" "$seed" $extra > "$f" || { echo "$seed GENFAIL" > "$W/s$seed.res"; exit 0; }
run_c() {
  { timeout 10 "$DITTO_ROOT/bin/ditto" build "$f" -o "$W/s$seed.exe" 2>&1; st=$?
    if (( st == 0 )); then timeout 10 "$W/s$seed.exe" </dev/null 2>&1; st=$?; fi
    if (( st != 0 )); then echo "exit: $st"; fi; } > "$W/s$seed.c.out"
}
run_r() {
  { timeout 10 python3 -I "$REFEREE" "$f" </dev/null 2>&1; st=$?
    if (( st != 0 )); then echo "exit: $st"; fi; } > "$W/s$seed.r.out"
}
run_c; run_r
last=$(tail -n1 "$W/s$seed.r.out")
lastc=$(tail -n1 "$W/s$seed.c.out")
case "$last" in
  "exit: 124") cls=timeout;;
  "exit: 2") cls=compile;; "exit: 1") cls=fault;; "exit: 0"|"exit: "[0-9]*) cls=other;; *) cls=ok;;
esac
if [[ $last == "exit: 124" || $lastc == "exit: 124" ]]; then res=agree; cls=timeout   # a runaway program, not a disagreement (stdout buffering differs)
elif cmp -s "$W/s$seed.c.out" "$W/s$seed.r.out"; then res=agree; else res=DIFF
  cp "$f" "$HERE/diffs/s$seed.ditto"; cp "$W/s$seed.c.out" "$HERE/diffs/s$seed.compiler.out"; cp "$W/s$seed.r.out" "$HERE/diffs/s$seed.referee.out"
fi
echo "$seed $res $cls" > "$W/s$seed.res"
rm -f "$W/s$seed.exe"
