# kind: fault
# perl returns three values to a list, and aaa to a scalar (T143): a list
# repeated is list-shaped (D18). By hand.
use v5.42;
sub three() {
    return ("a") x 3;
}
my $s = three();
say $s;
