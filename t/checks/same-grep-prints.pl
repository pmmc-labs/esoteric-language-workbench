# check: fails: without sort
# A block that prints, between the sort and its keys.
use v5.42;
my %h = (pear => 3, apple => 1, fig => 2, plum => 4);
my @s = sort grep { say $_; 1 } keys %h;
say scalar(@s);
