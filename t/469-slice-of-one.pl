# kind: refused
# perl warns as it compiles: Scalar value @a[0] better written as $a[0] (T167).
use v5.42;
my @a = (1, 2, 3);
my @s = @a[0];
