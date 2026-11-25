# kind: refused
# perl warns: Useless use of multiplication (*) in void context (T140).
use v5.42;
sub f($x) {
    $x * 2;
    return 1;
}
say f(2);
