# kind: refused
# perl takes it; with more after the bracket it warns (T190, D87).
use v5.42;
my @a = (3, 1, 2);
my @r = sort(@a);
