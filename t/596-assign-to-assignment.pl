# kind: refused
# perl assigns to $x twice (D56).
use v5.42;
my $x;
($x = 5) = 7;
