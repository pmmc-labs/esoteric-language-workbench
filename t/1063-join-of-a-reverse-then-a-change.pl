# kind: refused
# perl: 3-2-50-7 (T185).
use v5.42;
my @a = (1, 2, 3);
sub chg() {
    $a[0] = 50;
    return 7;
}
say join("-", reverse(@a), chg());
