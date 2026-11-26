#!/bin/sh
# Every finding's program under perl 5.42, plain: writes outputs.txt.
#     sh docs/briefs/step12-review/run-all.sh
cd "$(dirname "$0")" || exit 1
PERL=${CURLY_PERL:-/opt/perl-5.42/bin/perl}
: > outputs.txt
for f in w1 w2 p1 p2 p3 p4 g1 g2 g3 c3; do
    {
        echo "== $f.pl"
        timeout 10 "$PERL" "$f.pl" 2>&1
        echo "[exit $?]"
    } >> outputs.txt
done
cat outputs.txt
