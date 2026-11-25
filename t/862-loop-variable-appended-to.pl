# kind: refused
# perl: 1z2z (D17).
use v5.42;
my @a = (1, 2);
for my $x (@a) {
    $x .= "z";
}
say @a;
