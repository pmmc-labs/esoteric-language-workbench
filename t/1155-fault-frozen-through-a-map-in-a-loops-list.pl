# kind: fault
# A loop's list names every array anywhere in it, a map's own list too
# (D80): perl would have walked copies here, and the language is the
# stricter. By hand.
use v5.42;
my @a = (1, 2);
say 1;
for my $x (map { $_ } @a) {
    say $x;
}
for my $x (map { $_ } @a) {
    push @a, 1;
    last;
}
say 2;
