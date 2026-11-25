use v5.42;
# Lists the proposal says freeze nothing, and perl walks the array through.
my @a = (1, 2, 3);
for my $x ((@a) x 2) { $a[0] = 9; say $x; }
@a = (1, 2, 3);
for my $x ((@a)[0, 1]) { $a[0] = 9; say $x; }
@a = (1, 2, 3);
for my $x ((@a, 5)[0]) { $a[0] = 9; say $x; }
@a = (1, 2, 3);
my @b = (4);
for my $x (@a && @b) { $b[0] = 9; say $x; }
@a = (1, 2, 3);
for my $x ($a[0] = 5, ++$a[1], $a[2] .= "x") { $a[0] = 9; $a[1] = 9; $a[2] = 9; say $x; }
@a = (1, 2, 3);
for my $x ($#a) { push @a, 7; say $x; }
@a = (1, 2, 3);
for my $x (@a || @b) { say $x; }
