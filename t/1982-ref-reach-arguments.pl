# kind: refused
# perl runs it: '55\n'.
use v5.42;
my $r = [1, 2];
sub f($x, $y) {
    return $x . $y;
}
say f($r->[0], ($r->[0] = 5));
