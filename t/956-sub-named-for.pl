# kind: refused
# perl takes the definition, and a call of it, 1 + for(3), does not compile (T28).
use v5.42;
sub for($p) { return $p + 10; }
say 1;
