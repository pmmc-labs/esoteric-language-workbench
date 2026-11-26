use v5.42;
my $cnt = 0; sub tick { $cnt++ } tick() for 1..3; { my $cnt = 100; tick(); } print "$cnt\n";
