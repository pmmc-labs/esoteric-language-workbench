use v5.42;
my $cnt=0; sub bump { $cnt++ } bump(); bump(); print "$cnt\n";
