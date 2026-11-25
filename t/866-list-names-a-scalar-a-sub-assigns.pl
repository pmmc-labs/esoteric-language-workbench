# kind: refused
# Through a sub the block calls: perl prints 1 and 9 (D77).
use v5.42;
my $p = 1;
my $q = 2;
sub bump() {
    $q = 9;
    return 0;
}
for my $x ($p, $q) {
    bump();
    say $x;
}
