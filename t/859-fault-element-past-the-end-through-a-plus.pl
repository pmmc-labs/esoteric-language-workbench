# kind: fault
# A unary plus hands it on (T161). By hand.
use v5.42;
my @a = (1, 2, 3);
say 1;
for my $x (+$a[2]) {
    say $x;
}
for my $x (+$a[3]) {
    say $x;
}
say 2;
