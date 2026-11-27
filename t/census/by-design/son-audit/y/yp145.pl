use v5.42;
my ($x,$y)=(1,2); my $r = \($x = $y); $$r = 7; print "$x $y\n";
