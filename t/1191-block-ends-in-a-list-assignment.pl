# kind: refused
# A list assignment has no value (D78).
use v5.42;
my @a = (1, 2);
my @r = map { my @q = ($_, 1) } @a;
