# kind: refused
# perl does not compile it (T168).
use v5.42;
my @a = (1, 2, 3);
@a += 1;
