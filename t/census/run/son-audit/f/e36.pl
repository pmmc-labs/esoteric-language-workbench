use v5.42;
my $r = do { eval { die "x\n" }; $@ ? "e" : "n" }; print "$r\n";
