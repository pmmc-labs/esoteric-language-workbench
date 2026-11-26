# kind: refused
# perl: 51.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my %g = (5 => 1);
my @l = ($h{a}, exists $g{$h{a} = 5});
say @l;
