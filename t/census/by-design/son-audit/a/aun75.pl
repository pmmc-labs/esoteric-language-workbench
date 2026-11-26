use v5.42;
our $g = 1; sub t { local $g = 2; eval { die "x\n" }; $g } print t(), $g, "\n";
