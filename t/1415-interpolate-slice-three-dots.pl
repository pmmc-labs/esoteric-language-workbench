# kind: refused
# perl prints 1 2.
use v5.42;
my @a = (1, 2, 3);
say "@a[0 ... 1]";
