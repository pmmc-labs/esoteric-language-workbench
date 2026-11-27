# kind: fault
# A change to an array a foreach is over is a fault, and not caught (D13).
use v5.42;
my @a = (1, 2);
for my $x (@a) {
    say $x;
    try { push @a, 3 } catch ($e) { say "caught" }
    last;
}
