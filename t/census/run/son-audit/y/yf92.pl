use v5.42;
my $x=1; my $y = do { $x++; $x * 2 }; print "$x $y\n";
