# kind: refused
# perl warns: Scalar value @a[...] better written as $a[...] (T206).
use v5.42;
my @a = (1, 2, 3);
my $i = 1;
say "@a[$i]";
