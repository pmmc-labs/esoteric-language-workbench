# kind: refused
# perl runs it, and nothing is done.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
exists $h{a};
