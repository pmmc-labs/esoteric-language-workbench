# kind: refused
# D76 in a loop's list: perl prints 1 and 1, the element read after the shift.
use v5.42;
my @a = (1, 2);
for my $x ($a[0], shift(@a)) {
    say $x;
}
