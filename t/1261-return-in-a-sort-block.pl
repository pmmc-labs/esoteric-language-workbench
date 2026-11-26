# kind: refused
# perl ends the comparison, not the sub: this gives 0 (T174).
use v5.42;
sub f() {
    my @s = sort { return 5 } (3, 1, 2);
    return 0;
}
