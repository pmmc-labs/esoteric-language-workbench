# kind: refused
# perl takes it, in silence: @b has 2 and 3, and $z is undef (T168).
use v5.42;
my ($m, @b, $z) = (1, 2, 3);
say $m;
