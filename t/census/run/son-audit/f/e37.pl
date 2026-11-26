use v5.42;
sub f { eval { die "x\n" }; $@ } my $e = f(); eval { 1 }; print $e;
