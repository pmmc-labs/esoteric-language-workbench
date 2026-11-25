# kind: refused
# perl does not compile a call of it (T28).
use v5.42;
sub for($p) { return $p + 10; }
say 1;
