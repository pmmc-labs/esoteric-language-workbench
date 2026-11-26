# check: fails: line 5: keys without sort
# One element of the copy is one of perl's own choosing.
use v5.42;
my %h = (pear => 3, apple => 1, fig => 2, plum => 4);
my @k = keys %h;
say join(",", sort @k), $k[0];
