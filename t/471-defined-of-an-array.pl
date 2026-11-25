# kind: refused
# perl does not compile it: Can't use 'defined(@array)' (T168).
use v5.42;
my @a = (1, 2, 3);
say defined(@a) ? 1 : 0;
