# kind: refused
# perl's each: a. Not in the language (D101).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
while (my ($k, $v) = each %h) { say $k if $k eq "a"; }
