# kind: refused
# perl runs it: '2\n'.
use v5.42;
my $s = [9];
sub f($t) {
    $t->[0] = 1;
    return 1;
}
say $s->[0] + f($s);
