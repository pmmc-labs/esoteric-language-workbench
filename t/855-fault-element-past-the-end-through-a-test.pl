# kind: fault
# A branch of ? : in a foreach's list is the element itself, to perl, which makes it (T161). By hand.
use v5.42;
my @a = (1, 2, 3);
say 1;
for my $x (1 ? $a[2] : 0) {
    say $x;
}
for my $x (1 ? $a[3] : 0) {
    say $x;
}
say 2;
