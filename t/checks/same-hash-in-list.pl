# check: fails: line 5: a whole hash without sort
# A hash in a list is its keys and values in perl's order.
use v5.42;
my %h = (a => 1);
say join ",", %h;
