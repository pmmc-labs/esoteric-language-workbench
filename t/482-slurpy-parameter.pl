# kind: refused
# perl takes the rest of the arguments into @r: step 10.
use v5.42;
sub f($x, @r) { return $x; }
say f(1, 2, 3);
