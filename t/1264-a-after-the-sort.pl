# kind: refused
# Outside the block there is no $a.
use v5.42;
my @a = (3, 1, 2);
my @r = sort { $a <=> $b } @a;
say $a;
