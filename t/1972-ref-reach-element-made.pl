# kind: refused
# perl runs it, and says nothing.
use v5.42;
my @a = (undef);
my @l = ($a[0], ($a[0][0] = 1));
