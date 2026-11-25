# kind: refused
# perl does not compile it (T137).
use v5.42;
sub f($x, $y) { return $x + $y; }
say f(,1,2);
