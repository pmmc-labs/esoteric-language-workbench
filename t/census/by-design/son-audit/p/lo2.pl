use v5.42;
our $g = 1; sub t { local $g = 2; die "x\n" } eval { t() }; print "$g\n";
