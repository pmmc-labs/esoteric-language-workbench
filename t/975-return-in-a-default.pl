# kind: refused
# perl prints 7 (T139).
use v5.42;
sub f($x = return 7) { return $x; }
say f();
