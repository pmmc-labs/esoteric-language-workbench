# kind: refused
# a slice of keys and values, to perl: 2.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my %g = %h{"a", "b"};
say scalar(%g);
