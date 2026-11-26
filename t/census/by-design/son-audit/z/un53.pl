use v5.42;
our $g=1; eval { local $g; die "x\n" }; print "$g\n";
