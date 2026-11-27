# kind: dies
# From the block of a sort, half way through.
use v5.42;
my @a = (3, 1, 2);
say "sorting";
my @b = sort { die "compared $a and $b" if $a == 2 || $b == 2; $a <=> $b } @a;
