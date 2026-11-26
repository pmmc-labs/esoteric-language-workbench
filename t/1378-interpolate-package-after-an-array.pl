# kind: refused
# perl reads @a::b, empty.
use v5.42;
my @a = (1, 2, 3);
say "@a::b";
