# kind: refused
# perl takes it, and changes nothing.
use v5.42;
my @a = (1, 2, 3);
@a[0, 1] += 1;
