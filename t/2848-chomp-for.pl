# kind: refused
# perl chomps each of the list through $_.
use v5.42;
my ($x, $y) = ("a\n", "b\n");
chomp for $x, $y;
