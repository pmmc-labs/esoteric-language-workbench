use v5.42;
my $r = eval { die "obj\n" } || do { chomp(my $e = $@); "caught($e)" }; print "$r\n";
