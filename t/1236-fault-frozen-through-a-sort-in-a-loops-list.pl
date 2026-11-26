# kind: fault
# perl's loop over a sort of an array is over the array's own elements, and
# a store to it shows in the loop: 7, 7, 7 (T6). The array is frozen. By hand.
use v5.42;
my @a = (3, 1, 2);
say 1;
for my $x (sort { $a <=> $b } @a) {
    say $x;
}
for my $x (sort { $a <=> $b } @a) {
    $a[0] = 7;
    say $x;
}
say 2;
