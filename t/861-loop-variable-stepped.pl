# kind: refused
# perl: 23 (D17).
use v5.42;
my @a = (1, 2);
for my $x (@a) {
    $x++;
}
say @a;
