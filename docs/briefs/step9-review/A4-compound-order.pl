use v5.42;
# A compound assignment works its target's index out before its right side,
# and the target is the container.
my @a = (1, 2, 3);
my $i = 0;
$a[$i] += ($i = 2);
say $a[0], " ", $a[1], " ", $a[2];
@a = (1, 2, 3);
$i = 0;
$a[$i] .= ($i = 2);
say $a[0], " ", $a[1], " ", $a[2];
@a = (0, 2, 3);
$i = 0;
$a[$i] ||= ($i = 2);
say $a[0], " ", $a[1], " ", $a[2];
@a = (1, 2, 3);
$a[0] += shift(@a);
say scalar(@a), ": ", $a[0], " ", $a[1];
@a = (1, 2, 3);
$a[$#a] += pop(@a);
say scalar(@a), ": ", $a[0], " ", $a[1];
@a = ();
$a[5] //= push(@a, 1);
say scalar(@a), ": ", $a[5], " ", $a[6];
@a = (1, 2, 3);
sub clr() { @a = (); return "x" }
$a[0] .= clr();
say scalar(@a);
