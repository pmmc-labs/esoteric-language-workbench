use v5.42;
my $x=9; my @a=(1,2); ($x, @a) = (@a, $x); print "$x @a\n";
