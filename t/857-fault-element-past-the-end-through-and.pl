# kind: fault
# The right side of && (T161). By hand.
use v5.42;
my @a = (1, 2, 3);
say 1;
for my $x (1 && $a[2]) {
    say $x;
}
for my $x (1 && $a[3]) {
    say $x;
}
say 2;
