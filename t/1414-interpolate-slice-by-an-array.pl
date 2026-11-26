# kind: refused
# perl prints 1 3.
use v5.42;
my @a = (1, 2, 3);
my @w = (0, 2);
say "@a[@w]";
