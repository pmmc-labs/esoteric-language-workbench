# A slurpy parameter: refused until step 10.
use v5.42;
sub f($x, @r) { return $x; }
say f(1, 2, 3);
