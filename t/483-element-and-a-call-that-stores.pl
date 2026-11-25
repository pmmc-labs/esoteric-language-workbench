# kind: refused
# perl prints 51: the element is read after chg has stored to it (T149, D76).
use v5.42;
my @a = (1, 2, 3);
sub chg() { $a[0] = 50; return 1; }
say $a[0] + chg();
