# kind: refused
# perl takes the blanks: 1 2 3.
use v5.42;
my @a = (1, 2, 3);
say "@{ a }";
