# kind: refused
# octal, to perl: the index 8, and an array of nine.
use v5.42;
my @a = (1, 2, 3);
@a[010, 1] = (1, 2);
say scalar(@a);
