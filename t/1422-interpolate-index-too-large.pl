# kind: refused
# perl prints 3: the last element (T211).
use v5.42;
my @a = (1, 2, 3);
say "$a[18446744073709551615]";
