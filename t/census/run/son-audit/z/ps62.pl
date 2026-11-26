use v5.42;
my $x=1; for (1..3) { $x = $x > 2 ? "big" : $x+1 } print "$x\n";
