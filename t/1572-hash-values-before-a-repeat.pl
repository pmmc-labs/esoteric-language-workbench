# kind: refused
# perl does not compile it: Type of arg 1 to values must be hash or array (T225).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say values %h x 2;
