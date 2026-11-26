# kind: refused
# octal, to perl: the key 8.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say exists $h{010} ? 1 : 0;
