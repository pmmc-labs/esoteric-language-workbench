use v5.42;
our @a=(1); sub t { local @a = (2,3); return scalar @a } print t(), scalar(@a), "\n";
