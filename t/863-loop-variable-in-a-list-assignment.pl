# kind: refused
# perl: 88 (D17).
use v5.42;
my @a = (1, 2);
my $y;
for my $x (@a) {
    ($x, $y) = (8, 9);
}
say @a;
