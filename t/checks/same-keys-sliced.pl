# check: fails: without sort
# One key picked before the sort.
use v5.42;
my %h = (pear => 3, apple => 1, fig => 2, plum => 4);
say join ",", sort { $a cmp $b } (keys %h)[0];
