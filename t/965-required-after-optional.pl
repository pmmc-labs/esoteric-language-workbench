# kind: refused
# perl: Mandatory parameter follows optional parameter.
use v5.42;
sub f($x = 1, $y) { return $x; }
