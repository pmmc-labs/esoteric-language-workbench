use v5.42;
# Targets perl takes that the proposal's sentence doesn't name.
my @a = (1, 2);
my ($x, $y) = (0, 0);
(($x), $y) = (5, 6);
say $x, " ", $y;
(($x, $y), @a) = (1, 2, 3);
say $x, " ", $y, " ", scalar(@a);
(+$x, $y) = (3, 4);
say $x;
($x ? $x : $y, $a[0]) = (1, 2);
say $x, " ", $a[0];
@a = (1, 2);
($x, $#a) = (5, 0);
say scalar(@a);
my ($m, @b, $z) = (1, 2, 3);
say scalar(@b), defined($z) ? 1 : 0;
my (@c, @d) = (1, 2, 3);
say scalar(@c), scalar(@d);
