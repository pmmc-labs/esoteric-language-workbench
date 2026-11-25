# kind: fault
# A loop over a reverse of an array is over the array's own elements, to perl
# (T6): frozen. By hand.
use v5.42;
my @a = (1, 2);
say 1;
for my $x (reverse @a) {
    say $x;
}
for my $x (reverse @a) {
    push @a, 1;
    last;
}
say 2;
