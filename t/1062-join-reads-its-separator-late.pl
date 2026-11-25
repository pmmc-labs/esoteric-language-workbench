# kind: refused
# perl: 1+2+3 (T186, D87).
use v5.42;
my $sep = "-";
sub chs() {
    $sep = "+";
    return 1;
}
say join($sep, chs(), 2, 3);
