use v5.42;
# A list repeat where one value is wanted is its last value, repeated.
my @c = (1, 2) x 2 x 2;
say scalar(@c), " ", $c[0];
@c = ((1, 2) x 2) x 2;
say scalar(@c);
@c = -(1) x 3;
say scalar(@c), " ", $c[0];
my $n = 2;
@c = ($n + 1) x 3;
say scalar(@c);
my @a = (4, 5, 6);
my $s = (@a) x 2;
say $s;
