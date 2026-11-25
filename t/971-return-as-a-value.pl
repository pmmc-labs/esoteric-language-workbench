# kind: refused
# perl prints 5 (T139).
use v5.42;
sub f() {
    my $x = return 5;
    return 9;
}
say f();
