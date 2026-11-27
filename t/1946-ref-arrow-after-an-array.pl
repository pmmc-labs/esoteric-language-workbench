# kind: refused
# perl dies: Can't use an array as a reference.
use v5.42;
my @a = (1, 2, 3);
say @a->[0];
