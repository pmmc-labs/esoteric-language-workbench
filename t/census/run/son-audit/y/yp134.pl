use v5.42;
my ($x,$y)=(1,"2a"); ($x = $y) =~ s/2/9/; print "$x $y\n";
