#!/bin/sh
# Every probe here under perl 5.42, plain: writes NAME.out beside each NAME.t.
#     sh docs/briefs/step13-review/run-all.sh
cd "$(dirname "$0")" || exit 1
for t in *.t; do
    python3 probe.py "$t" > "${t%.t}.out"
done
grep -c '^### ' *.out
