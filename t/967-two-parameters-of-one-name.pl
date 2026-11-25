# kind: refused
# perl warns as it compiles, and the second wins (T141).
use v5.42;
sub f($x, $x) { return $x; }
say f(1, 2);
