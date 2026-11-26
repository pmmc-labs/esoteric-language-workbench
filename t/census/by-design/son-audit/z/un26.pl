use v5.42;
my $x=1; eval { $x++; die "a\n" }; print "$x\n";
