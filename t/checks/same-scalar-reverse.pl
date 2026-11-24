# check: fails: line 5: keys without sort
# scalar reverse joins the keys, in their order, and turns them round.
use v5.42;
my %h = (a => 1);
say scalar reverse keys %h;
