# kind: refused
# perl prints 1 2 2 (T197).
use v5.42;
my @a = (1, 2, 3);
my $i = 1;
$i = 0;
say "$i $a[$i++] $i";
