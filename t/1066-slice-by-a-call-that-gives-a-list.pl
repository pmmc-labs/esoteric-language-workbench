# kind: refused
# Where one value is wanted perl gives the last of the slice: 5.
use v5.42;
sub two() {
    return (1, 0);
}
my $x = (5, 6, 7)[two()];
say $x;
