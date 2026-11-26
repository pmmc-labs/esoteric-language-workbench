# kind: refused
# A sort's block ends in a value.
use v5.42;
my @a = (3, 1, 2);
my @r = sort { say $a } @a;
