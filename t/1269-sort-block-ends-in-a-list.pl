# kind: refused
# perl takes the last, and warns.
use v5.42;
my @a = (3, 1, 2);
my @r = sort { ($a, $b) } @a;
