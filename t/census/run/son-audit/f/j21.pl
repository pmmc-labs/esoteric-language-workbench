use v5.42;
our ($x,$y)=(1,2); for my $r (\$x,\$y) { $$r*=3 } print "$x $y\n";
