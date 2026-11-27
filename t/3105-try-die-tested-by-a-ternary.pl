# kind: refused
# perl warns of a precedence problem.
use v5.42;
my $x = die("x") ? 1 : 2;
