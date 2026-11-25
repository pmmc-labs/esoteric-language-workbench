# kind: fault
# The second arm of ? : alone is list-shaped, and it is not the one taken. By hand.
use v5.42;
my @a = (4, 5, 6);
sub f() {
    return 1 ? 0 : @a;
}
say 1;
say f();
my $x = f();
say 2;
