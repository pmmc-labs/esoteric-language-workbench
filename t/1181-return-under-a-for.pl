# kind: refused
# perl: 4 (T191).
use v5.42;
sub f() {
    return $_ for 4, 5;
    return 0;
}
