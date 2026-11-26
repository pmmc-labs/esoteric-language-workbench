# check: fails: line 6: values without sort
# The array is sorted once and printed once as it is: the order shows.
use v5.42;
my %h = (pear => 3, apple => 1, fig => 2, plum => 4);
my @sorted = (1);
my @v = values %h;
say join(",", sort { $a <=> $b } @v);
say "@sorted", @v;
