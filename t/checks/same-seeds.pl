# check: fails: changes from run to run
# It sorts, so the reading rule passes it, and the sort leaves its ties
# as they came (a test with a sort in it breaks its ties): only running
# it under more than one seed shows the order is perl's.
use v5.42;
my %h = map { $_ => 1 } 1 .. 20;
say join ",", sort { length($a) <=> length($b) } keys %h;
