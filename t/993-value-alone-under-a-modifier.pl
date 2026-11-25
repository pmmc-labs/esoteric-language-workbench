# kind: refused
# perl is silent, and the sub is worth its test when the test fails (T145).
use v5.42;
sub f($x, $c) {
    $x * 2 if $c;
}
f(1, 0);
