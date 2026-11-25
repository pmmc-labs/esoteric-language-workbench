# kind: refused
# perl: 4 (D77).
use v5.42;
my $p = 1;
for my $x ($p) {
    for my $y (1) {
        $p = 4;
    }
    say $x;
}
