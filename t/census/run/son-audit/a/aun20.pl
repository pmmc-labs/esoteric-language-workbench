use v5.42;
my ($x,$y)=(1,2); my $r=\$x; ($x,$y)=($y,$x); print "$$r $x $y\n";
