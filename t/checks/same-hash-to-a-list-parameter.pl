# check: fails: line 6: a whole hash without sort
# A sub that takes a list is handed the hash in perl's order.
use v5.42;
my %h = (pear => 3, apple => 1, fig => 2, plum => 4);
sub first($x, @rest) { return $rest[0]; }
say first(1, %h);
