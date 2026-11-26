use v5.42;
my $s=""; for (1..3) { eval { die "x\n" if $_==2; $s.=$_ } } print "$s\n";
