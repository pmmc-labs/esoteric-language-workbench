# kind: refused
# sort hands on the elements themselves: perl prints 12507 (T185, D87).
use v5.42;
my @a = (3, 1, 2);
sub chg() {
    $a[0] = 50;
    return 7;
}
my @r = ((sort { $a <=> $b } @a), chg());
say @r;
