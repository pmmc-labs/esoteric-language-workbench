# kind: refused
# perl does not compile it: %a is not declared.
use v5.42;
my @a = (1, 2, 3);
say "@a{0}";
