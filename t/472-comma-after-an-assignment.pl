# kind: refused
# perl's comma operator: one element, and two warnings (T168).
use v5.42;
my @a = 1, 2, 3;
say scalar(@a);
