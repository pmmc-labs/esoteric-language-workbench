# kind: refused
# perl: Optional parameter lacks default expression.
use v5.42;
sub f($x =) { return $x; }
