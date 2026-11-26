# kind: refused
# perl: 5.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
@h{"x", delete($h{a})} = ($h{a}, 2);
say scalar(%h);
