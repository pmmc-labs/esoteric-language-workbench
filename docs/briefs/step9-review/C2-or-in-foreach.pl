use v5.42;
# Through `||` a foreach is over the count on the left, and the array on the right.
my @a = (1, 2, 3);
my @b = (4);
my @e;
for my $x (@a || @b) { say $x; }
for my $x (@e || @b) { $b[0] = 9; say $x; }
