use v5.42;
# A slice of an empty list is empty, whatever the indexes.
my @e;
my @b = (@e)[0, 1];
say scalar(@b);
@b = (@e)[0];
say scalar(@b);
@b = (1, 2, 3)[5, 6];
say scalar(@b);
@b = (1, 2, 3)[5];
say scalar(@b);
sub f($x = "d", $y = "d") { return $x . $y }
say f((@e)[0]);
say f((@e)[0, 1]);
sub first() { return (@e)[0] }
sub last1() { (@e)[0] }
my @c = first();
say scalar(@c);
@c = last1();
say scalar(@c);
@c = (first(), first(), 5);
say scalar(@c);
my $v = first();
say defined($v) ? 1 : 0;
