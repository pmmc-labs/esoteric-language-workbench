# kind: refused
# A call that gives a list makes the arguments a list, which is copied: so
# what an earlier argument names may not be changed by it. perl hands f the 9.
use v5.42;
my $v = 5;
sub two() {
    $v = 9;
    return (1, 2);
}
sub f($p, @r) {
    return $p;
}
say f($v, two());
