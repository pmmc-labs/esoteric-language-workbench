# kind: refused
# The assignment is inside a sum (D77).
use v5.42;
my $p = 1;
for my $x ($p) {
    say $x + ($p = 2);
}
