# kind: refused
# perl runs it: 'x1\n'. A store through a reference in a sub's catch counts for D109.
use v5.42;
my $s = [9];
sub f($t) {
    try { die "d\n"; } catch ($e) { $t->[0] = "x"; }
    return 1;
}
say $s->[0], f($s);
