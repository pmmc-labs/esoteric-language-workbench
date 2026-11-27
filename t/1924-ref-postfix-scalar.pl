# kind: refused
# perl dies: Not a SCALAR reference.
use v5.42;
my $r = [1, 2];
say $r->$*;
