# kind: refused
# perl runs it: 'x1\n'.
use v5.42;
my $s = [9];
sub f($t) {
    $t->[0] = "x";
    return 1;
}
say $s->[0] . f($s);
