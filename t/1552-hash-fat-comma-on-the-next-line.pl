# kind: refused
# perl reads a version string: the key A (T224).
use v5.42;
my %g = (v65
  => 1);
say join(",", sort keys %g);
