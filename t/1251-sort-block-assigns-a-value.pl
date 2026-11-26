# kind: refused
# perl: 355 (T10).
use v5.42;
my @a = (3, 1, 2);
my @s = sort { $b = 5; 0 } @a;
say @a;
