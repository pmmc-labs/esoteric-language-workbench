# kind: refused
# perl warns: Multidimensional syntax $a[1,2] not supported (T202).
use v5.42;
my @a = (1, 2, 3);
say "$a[1,2]";
