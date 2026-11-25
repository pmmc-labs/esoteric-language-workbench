# kind: refused
# perl does not compile it: f is a file handle, the sub not yet seen (T136).
use v5.42;
say f (1);
sub f($x) { return $x + 1; }
