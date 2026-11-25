use v5.42;
# A whole array or a slice in a list is its elements, read when the list is used.
my @a = (1, 2, 3);
sub chg() { $a[0] = 50; return 5 }
my @b = (@a, chg());
say $b[0], " ", $b[1], " ", $b[2], " ", $b[3];
$a[0] = 1;
say @a, chg();
$a[0] = 1;
@b = (@a[0, 1], chg());
say $b[0], " ", $b[1], " ", $b[2];
$a[0] = 1;
@b = ($a[0], chg());
say $b[0], " ", $b[1];
$a[0] = 1;
say $a[0], chg();
$a[0] = 1;
for my $x (@a, chg()) { say $x; }
sub grow() { push @a, 4; return 5 }
@a = (1, 2, 3);
@b = (@a, grow());
say scalar(@b), " ", scalar(@a);
