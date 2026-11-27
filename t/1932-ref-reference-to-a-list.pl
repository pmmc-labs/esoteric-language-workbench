# kind: refused
# perl runs it, and says nothing.
use v5.42;
my ($x, $y) = (1, 2);
my @s = \($x, $y);
