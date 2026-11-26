# kind: refused
# perl takes it, as map EXPR, LIST (D85, D87).
use v5.42;
my @r = map($_ * 2, 1, 2);
