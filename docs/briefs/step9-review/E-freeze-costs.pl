use v5.42;
# Loops the freeze faults, where perl prints what a copy would.
my @a = (1, 2, 3);
my $i = 0;
for my $x (@a) { $a[$i] = $x * 2; $i++; }
say $a[0], $a[1], $a[2];
my @b = (1, 2, 3);
for my $x (@b) { if ($x == 2) { push @b, 9; last; } }
say scalar(@b);
my @c = (3, 1, 2);
for my $x (@c) { if ($x == 1) { @c = (); last; } }
say scalar(@c);
my @d = (1, 2, 3);
my $sum = 0;
for my $x (@d) { if ($x == 3) { $sum += pop(@d); } }
say $sum;
my @q = (1, 2, 3);
for my $x (@q) { $q[2] = 3; }
say $q[2];
