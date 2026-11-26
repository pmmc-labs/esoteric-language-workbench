# kind: refused
# perl: 9, and reads a value that was freed (D102).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my @l = (%h, delete($h{a}));
say scalar(@l);
