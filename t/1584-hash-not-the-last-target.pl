# kind: refused
# perl gives the hash everything: 1.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my (%g, $x) = (a => 1);
say scalar(%g);
