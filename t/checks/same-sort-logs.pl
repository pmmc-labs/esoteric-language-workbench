# check: fails: without sort
# A comparator that prints shows the pairs it was given, in the hash's
# order.
use v5.42;
my %h = (pear => 3, apple => 1, fig => 2, plum => 4);
my @s = sort { print "$a$b\n"; $a cmp $b } keys %h;
say scalar(@s);
