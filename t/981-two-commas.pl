# kind: refused
# perl prints 3: two arguments (T137).
use v5.42;
sub f($x, $y) { return $x + $y; }
say f(1,,2);
