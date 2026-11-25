# kind: refused
# perl warns, and prints 1: the length of the count (T168).
use v5.42;
my @a = (1, 2, 3);
say length(@a);
