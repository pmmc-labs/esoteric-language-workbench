# kind: refused
# perl takes last for an expression: this leaves the loop when $i is 2,
# and prints 1 (T120, D62).
use v5.42;
my $i = 0;
while ($i++ < 3) {
    $i == 2 and last;
    print $i;
}
