# kind: refused
# perl takes the last, and warns (T176).
use v5.42;
my @a = (1, 2);
my @r = grep { ($_, 0) } @a;
