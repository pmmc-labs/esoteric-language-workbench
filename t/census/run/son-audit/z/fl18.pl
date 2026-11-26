use v5.42;
my $x=0; my $z=($x++, $x++)[0]; print "$x$z\n";
