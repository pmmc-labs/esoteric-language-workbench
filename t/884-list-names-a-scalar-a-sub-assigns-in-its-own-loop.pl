# kind: refused
# What a sub changes counts where it is inside a loop of the sub's own (D77).
use v5.42;
my $p = 1;
my $q = 2;
sub bump() {
    for my $i (1, 2) {
        $q = $i;
    }
    return 0;
}
for my $x ($p, $q) {
    bump();
    say $x;
}
