# kind: refused
# perl: 1 2 3 4.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my @l = sort values %h;
say "@l";
