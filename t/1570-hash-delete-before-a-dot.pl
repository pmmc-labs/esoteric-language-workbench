# kind: refused
# perl dies: delete argument is not a HASH or ARRAY element or slice (T220).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say delete $h{a} . "x";
