# kind: refused
# The same through brackets (T136).
use v5.42;
say((f (1)));
sub f($x) { return $x + 1; }
