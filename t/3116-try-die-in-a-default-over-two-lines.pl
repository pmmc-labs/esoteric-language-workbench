# kind: refused
# perl: the parameter's line.
use v5.42;
sub f($y =
  die "d") { return $y; }
say f(1);
