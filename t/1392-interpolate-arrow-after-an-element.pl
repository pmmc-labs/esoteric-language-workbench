# kind: refused
# perl dies: not an ARRAY reference (T203).
use v5.42;
my @a = (1, 2, 3);
say "$a[0]->[0]";
