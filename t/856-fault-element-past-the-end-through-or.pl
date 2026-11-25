# kind: fault
# The right side of || in a foreach's list is the element itself (T161). By hand.
use v5.42;
my @a = (1, 2, 3);
say 1;
for my $x (0 || $a[2]) {
    say $x;
}
for my $x (0 || $a[3]) {
    say $x;
}
say 2;
