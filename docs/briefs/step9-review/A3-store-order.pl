use v5.42;
# `=`: the right side's calls run first, then the target's index; what the
# right side *names* is read after that.
my @a = (1, 2, 3);
my $i = 0;
$a[$i] = ($i = 2);
say $a[0], " ", $a[1], " ", $a[2];
@a = (7, 7, 7);
$i = 0;
$a[$i++] = $i;
say $a[0], " ", $a[1], " ", $a[2];
@a = (1, 2, 3);
my $g = 7;
sub ix() { $g = 8; return 1 }
$a[ix()] = $g;
say $a[0], " ", $a[1], " ", $a[2];
@a = (1, 2, 3);
sub bump() { $a[0] = 99; return 1 }
$a[bump()] = $a[0];
say $a[0], " ", $a[1], " ", $a[2];
@a = (1, 2, 3);
$g = 7;
my $q;
($a[ix()], $q) = ($g, 1);
say $a[0], " ", $a[1], " ", $a[2];
@a = (1, 2, 3);
($a[bump()], $q) = ($a[0], 0);
say $a[0], " ", $a[1], " ", $a[2];
@a = (1, 2, 3);
$i = 0;
($i, $a[$i]) = (1, 5);
say $a[0], " ", $a[1], " ", $a[2], " ", $i;
