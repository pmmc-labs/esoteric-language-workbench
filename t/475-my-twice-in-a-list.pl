# kind: refused
# perl warns as it compiles, and the second wins (T168).
use v5.42;
my ($x, $x) = (1, 2);
say $x;
