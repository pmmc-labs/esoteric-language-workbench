#!/bin/sh
# W4: runs w-lastassign.pl under perl 5.42 and under the compiler as it is
# (steps 0 to 12 built). The compiler prints false/undef/no in silence;
# D78 says a list assignment as a sub's last statement has no value (a fault).
#     sh docs/briefs/step14-review/curly-now.sh
cd "$(dirname "$0")" || exit 1
PERL=${CURLY_PERL:-/opt/perl-5.42/bin/perl}
out=$(mktemp -d)
echo "--- perl:"; "$PERL" w-lastassign.pl; echo "[exit $?]"
echo "--- curly:"
node ../../../bin/curlyc.ts -o "$out/w" w-lastassign.pl && "$out/w"; echo "[exit $?]"
rm -rf "$out"
