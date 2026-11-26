# kind: refused
# perl: a.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
for (%h) { say $_ if $_ eq "a"; }
