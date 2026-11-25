# kind: refused
# Two assignments joined by and, to perl, which warns of the first:
# Found = in conditional. A statement is one (D56).
use v5.42;
my $x;
my $y;
$x = 1 and $y = 2;
