# kind: refused
# perl prints 2 (T202).
use v5.42;
my @a = (1, 2, 3);
say "$a['1']";
