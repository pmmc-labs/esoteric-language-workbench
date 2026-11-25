# kind: fault
# A slice in a branch of ? : (T161). By hand.
use v5.42;
my @a = (1, 2, 3);
say 1;
for my $x (1 ? @a[0, 2] : @a) {
    say $x;
}
for my $x (1 ? @a[0, 3] : @a) {
    say $x;
}
say 2;
