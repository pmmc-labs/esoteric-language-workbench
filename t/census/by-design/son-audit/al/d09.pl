use v5.42;
my $x=1; sub bump { $_[0] *= 10 } bump($x = 4); print "$x\n";
