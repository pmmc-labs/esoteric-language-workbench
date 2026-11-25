# kind: fault
# A fault in the test of an elsif names the line of the elsif, not of the
# if or of the test: perl warns of this undef at line 10.
use v5.42;
my $u;
my $n = 0;
if ($n) {
    say "not reached";
}
elsif
    (
    $u * 2) {
    say "not reached";
}
