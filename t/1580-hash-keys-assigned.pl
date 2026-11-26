# kind: refused
# perl takes it, to make room: nothing printed.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
keys(%h) = 100;
