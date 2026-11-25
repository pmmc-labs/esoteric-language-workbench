# kind: refused
# perl does not compile it (T135).
use v5.42;
sub f($x) { return $x + 1; }
say 5-f(2);
