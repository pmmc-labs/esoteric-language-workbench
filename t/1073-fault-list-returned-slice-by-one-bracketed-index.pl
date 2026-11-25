# kind: fault
# A slice of an array is list-shaped whatever its indexes: perl gives the last of them. By hand.
use v5.42;
my @a = (4, 5, 6);
sub f() {
    return @a[(1)];
}
say 1;
say f();
my $x = f();
say 2;
