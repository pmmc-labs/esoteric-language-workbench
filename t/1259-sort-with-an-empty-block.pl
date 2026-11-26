# kind: refused
# perl: a syntax error (T175).
use v5.42;
my @a = (3, 1, 2);
my @r = sort { } @a;
