# kind: refused
# perl prints 12: the string reads $i late (T197).
use v5.42;
my @a = (1, 2, 3);
my $i = 1;
say "$i$a[$i = 2]";
