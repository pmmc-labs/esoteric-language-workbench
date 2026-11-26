# kind: refused
# perl dies: not a SCALAR reference.
use v5.42;
my $x = 3;
say "$$x";
