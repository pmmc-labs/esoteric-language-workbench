# kind: refused
# perl does not compile it: Slurpy parameter not last.
use v5.42;
sub f(%o, $x) { return 1 }
