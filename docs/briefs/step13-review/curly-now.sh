#!/bin/sh
# Programs run under perl and under today's compiler (step 12b), to see what the
# existing walks already do that step 13 builds on.
#     sh docs/briefs/step13-review/curly-now.sh
cd "$(dirname "$0")/../../.." || exit 1
PERL=${CURLY_PERL:-/opt/perl-5.42/bin/perl}
T=${TMPDIR:-/tmp}/step13-review-$$
mkdir -p "$T"
run() {
    printf 'use v5.42;\n%s\n' "$1" > "$T/x.pl"
    echo "=== $1"
    echo "--- perl:"; "$PERL" "$T/x.pl" 2>&1; echo "[exit $?]"
    echo "--- curly:"
    if node bin/curlyc.ts -o "$T/x" "$T/x.pl" 2>&1 | sed "s|$T/||"; [ -x "$T/x" ]; then "$T/x" 2>&1; echo "[exit $?]"; fi
    rm -f "$T/x"
}
# A default between arguments is a later part of the arguments (refused).
run 'my @a = (undef, 5);
sub g() { $a[1] = 99; return 0; }
sub f($x //= g(), $y = 0) { say $y; }
f(@a);'
run 'my ($p, $q) = (undef, 5);
sub g() { $q = 99; return 0; }
sub f($x //= g(), $y = 0) { say $y; }
f($p, $q);'
# A map, sort or grep block is a later part of the list it stands in (refused).
run 'my @a = (1); say $a[0], map { $a[0] = 9; 1 } (1);'
run 'my @a = (1); say $a[0], sort { $a[0] = 9; 0 } (1, 2);'
# The right side of = is read when the store happens (D14).
run 'my @a; my $x = 1; $a[$x = 2] = $x; say $a[2];'
# A target that changes a variable the right side names, in a list assignment (refused).
run 'my @a; my $x = 1; my $y; ($a[$x = 2], $y) = ($x, 1); say $a[2];'
# A bare block as a sub last statement is not a value.
run 'sub f() { { 1, 2 } } my @l = f(); say scalar(@l);'
# A builtin with no argument is refused.
run 'my @l = map { length } ("ab"); say "@l";'
rm -rf "$T"
