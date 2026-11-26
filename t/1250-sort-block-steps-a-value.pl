# kind: refused
# perl rewrites the array: 513 (T179, T10).
use v5.42;
my @a = (3, 1, 2);
my @s = sort { $a++; 0 } @a;
say @a;
