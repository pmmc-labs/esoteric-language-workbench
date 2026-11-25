# kind: refused
# perl prints 5: q(5) is a string, and the sub is never called (T28).
use v5.42;
sub q($x) { return $x * 2; }
say q(5);
