# kind: refused
# perl warns as it compiles, and prints 5 (T141).
use v5.42;
sub f($x) {
    my $x = 5;
    return $x;
}
say f(1);
