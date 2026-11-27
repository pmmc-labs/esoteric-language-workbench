# kind: refused
# perl chomps both.
use v5.42;
my ($x, $y) = ("a\n", "b\n");
chomp($x, $y);
