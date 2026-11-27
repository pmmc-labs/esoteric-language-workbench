# kind: refused
# perl ends the string at the first ")", and does not compile: Missing right curly or square bracket.
use v5.42;
my @a = (1, 2);
say qq($a[1)]);
