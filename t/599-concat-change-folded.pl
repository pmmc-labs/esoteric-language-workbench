# kind: refused
# perl folds the ? : away as it compiles, and what is left is one row
# of dots: 55, where one dot at a time gives 35 (T117, D57).
use v5.42;
my $x = 3;
say((1 ? $x . "" : 0) . ($x = 5));
