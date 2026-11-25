# kind: refused
# perl returns three values to a list, and aaa to a scalar (T143).
use v5.42;
sub three() {
    return ("a") x 3;
}
my $s = three();
say $s;
