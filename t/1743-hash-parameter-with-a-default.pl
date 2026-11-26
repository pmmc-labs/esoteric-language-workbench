# kind: refused
# perl does not compile it: A slurpy parameter may not have a default value.
use v5.42;
sub f(%o = (a => 1)) { return 1 }
