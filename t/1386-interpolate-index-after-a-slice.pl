# kind: refused
# perl does not compile it (T203).
use v5.42;
my @a = (1, 2, 3);
say "@a[0, 1][0]";
