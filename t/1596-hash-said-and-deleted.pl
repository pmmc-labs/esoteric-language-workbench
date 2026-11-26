# kind: refused
# perl: 11.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say $h{a}, delete $h{a};
