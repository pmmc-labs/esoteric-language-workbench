# kind: refused
# A my is seen from the statement after its own, so this $x is an
# outer one, and there is none (T58). perl doesn't compile it.
use v5.42;
my $x = $x;
