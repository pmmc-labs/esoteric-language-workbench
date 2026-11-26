# kind: refused
# perl does not compile it: a hash, to perl (T175, T210).
use v5.42;
my @a = (1, 2, 3);
my @b = map { "$_", 1 } @a;
