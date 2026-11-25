use v5.42;
# A scalar variable in a list is the variable, read when the list is used.
my $x = 1;
sub bump() { $x = 9; return 5 }
my @b = ($x, bump());
say $b[0], " ", $b[1];
$x = 1;
say $x, bump();
$x = 1;
my @a;
push @a, $x, bump();
say $a[0], " ", $a[1];
$x = 1;
my ($p, $q) = ($x, bump());
say $p, " ", $q;
$x = 1;
for my $y ($x, bump()) { say $y; }
my $i = 1;
@b = ($i, $i++);
say $b[0], " ", $b[1];
@b = ($i, ++$i);
say $b[0], " ", $b[1];
@b = ($i, $i = 7);
say $b[0], " ", $b[1];
$x = 1;
@b = (($x) x 2, bump());
say $b[0], " ", $b[1], " ", $b[2];
$x = 1;
@b = (($x, 0)[0, 1], bump());
say $b[0], " ", $b[1], " ", $b[2];
$x = 1;
@b = ((1 ? $x : 0), bump());
say $b[0], " ", $b[1];
