# kind: refused
# perl reads the element after the index has stored to it: 9 9 7.
use v5.42;
my @a = (1, 2, 3);
@a[0, ($a[1] = 9) - 7] = ($a[1], 7);
say "@a";
