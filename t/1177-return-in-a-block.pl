# kind: refused
# perl ends the sub from a map block (T174).
use v5.42;
sub f() {
    my @s = map { return 5 } (3, 1, 2);
    return 0;
}
