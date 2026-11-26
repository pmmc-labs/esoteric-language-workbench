# kind: refused
# grep hands on the elements themselves: perl prints 50237 (T185, D87).
use v5.42;
my @a = (1, 2, 3);
sub chg() {
    $a[0] = 50;
    return 7;
}
my @r = ((grep { 1 } @a), chg());
say @r;
