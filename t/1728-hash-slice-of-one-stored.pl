# kind: refused
# perl takes it, and warns nothing: 9 2 3.
use v5.42;
my @a = (1, 2, 3);
@a[0] = (9);
say "@a";
