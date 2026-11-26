# kind: refused
# perl runs it: it sets each's place back, and the language has no each (D101).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
keys %h;
