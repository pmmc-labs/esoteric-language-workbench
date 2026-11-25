# kind: refused
# perl calls it, the sub being written first; written after, it does not compile (D21).
use v5.42;
sub f() { say "f"; }
f;
