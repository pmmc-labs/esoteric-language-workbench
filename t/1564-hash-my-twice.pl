# kind: refused
# perl warns: "my" variable %h masks earlier declaration in same scope.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my %h = (z => 1);
say scalar(%h);
