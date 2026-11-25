# kind: refused
# perl doesn't compile it: Global symbol "$y" requires explicit package
# name.
use v5.42;
my $x = 1;
say $y;
