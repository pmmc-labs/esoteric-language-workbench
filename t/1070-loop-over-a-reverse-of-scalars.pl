# kind: refused
# D77 through reverse: perl prints 2 and 5.
use v5.42;
my $p = 1;
my $q = 2;
for my $x (reverse($p, $q)) {
    $p = 5;
    say $x;
}
