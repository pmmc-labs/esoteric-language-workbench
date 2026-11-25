# kind: refused
# perl walks the variables themselves: this prints 7 and 2 (D77, T13).
use v5.42;
my $p = 1;
my $q = 2;
for my $x ($p, $q) {
    $p = 7;
    say $x;
}
