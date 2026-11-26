# kind: refused
# perl takes a scalar first after sort for a sub to compare by (D21).
use v5.42;
my $x = 3;
my @r = sort $x, 1;
say @r;
