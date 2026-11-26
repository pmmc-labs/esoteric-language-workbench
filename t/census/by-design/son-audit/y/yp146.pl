use v5.42;
my ($x,$y)=(1,2); sub set { $_[0] = 7 } set($x = $y); print "$x $y\n";
