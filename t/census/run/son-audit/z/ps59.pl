use v5.42;
my $x=1; my $y=1; for (1..5) { ($x,$y)=($y,$x+$y) } print "$x $y\n";
