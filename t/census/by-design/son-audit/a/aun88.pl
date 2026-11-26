use v5.42;
my $x = 1; eval { $x = 2; die "x\n" }; print "$x\n";
