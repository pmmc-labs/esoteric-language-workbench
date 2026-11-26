# kind: refused
# perl prints 2.
use v5.42;
my @a = (1, 2, 3);
say "$a[$a[0]]";
