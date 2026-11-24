# check: fails: changes from run to run
# It sorts, so the reading rule passes it, and the sort changes nothing:
# only running it under more than one seed shows the order is perl's.
use v5.42;
my %h = map { $_ => 1 } 1 .. 20;
say join ",", sort { 0 } keys %h;
