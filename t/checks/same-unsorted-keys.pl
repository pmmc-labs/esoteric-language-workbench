# check: fails: line 6: keys without sort
# One key, so every seed agrees and the .expected is right: only reading
# the program shows that it prints a hash's order.
use v5.42;
my %h = (a => 1);
say join ",", keys %h;
