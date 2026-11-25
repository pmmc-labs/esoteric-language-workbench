# kind: refused
# perl returns both.
use v5.42;
sub f() {
    return 1, 2;
}
say f();
