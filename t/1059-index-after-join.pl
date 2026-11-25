# kind: refused
# perl does not compile it.
use v5.42;
my @a = (1, 2);
say join(",", @a)[0];
