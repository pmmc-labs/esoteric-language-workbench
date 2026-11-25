# kind: refused
# perl prints 1.
use v5.42;
sub f($c) {
    return 1 while $c;
    return 2;
}
say f(1);
