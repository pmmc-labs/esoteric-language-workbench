# kind: refused
# perl makes the list 50 2 3 1: the array is flattened after chg has run (T157, D76).
use v5.42;
my @a = (1, 2, 3);
sub chg() { $a[0] = 50; return 1; }
my @b = (@a, chg());
say $b[0];
