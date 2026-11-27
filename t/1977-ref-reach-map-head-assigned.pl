# kind: refused
# perl crashes (a segmentation fault).
use v5.42;
my $r = [1, 2];
my @l = map { $r = [7]; $_ } ($r->[0], $r->[1]);
