# kind: refused
# perl takes the backslash away first: Y, the element (T278).
use v5.42;
my $x = "X";
my @x = ("Y");
say qq[$x\[0\]];
