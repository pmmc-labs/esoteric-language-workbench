# kind: fault
# A store in a try through a copy of what a loop's list reads through is the freeze's fault, never caught (D13, T251).
use v5.42;
my $r = [1, 2];
my $q = $r;
for my $x ($r->[0]) {
    try { $q->[0] = 7; } catch ($e) { say "caught"; }
    last;
}
say "after";
