# kind: refused
# perl reads the element after the store in the keys: y 1 2.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my %g = (x => 1, y => 2);
my @l = ($h{a}, delete @g{"x", ($h{a} = "y")});
say "@l";
