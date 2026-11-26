# kind: refused
# perl 5.42 does not compile it: Multidimensional hash lookup is disabled.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say defined($h{1, 2}) ? 1 : 0;
