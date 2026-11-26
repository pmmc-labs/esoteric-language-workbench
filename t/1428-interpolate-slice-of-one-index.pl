# kind: refused
# perl warns: Scalar value @a[0] better written as $a[0] (T206).
use v5.42;
my @a = (1, 2, 3);
say "@a[0]";
