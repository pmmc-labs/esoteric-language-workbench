# kind: refused
# perl: 55.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my @l = ($h{a}, $h{a} = 5);
say @l;
