# kind: refused
# perl runs it: 'x1\n'. A store through a reference in a sub's try counts for D109.
use v5.42;
my $s = [9];
sub f($t) {
    try { $t->[0] = "x"; } catch ($e) { }
    return 1;
}
say $s->[0], f($s);
