# kind: refused
# perl rewrites the array: 24 (D17, T180).
use v5.42;
my @a = (1, 2);
for (@a) {
    $_ *= 2;
}
say @a;
