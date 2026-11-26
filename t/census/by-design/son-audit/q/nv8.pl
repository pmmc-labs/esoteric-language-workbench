use v5.42;
our @g = (1); sub t { local @g = (@g, 2); return scalar @g } print t(), scalar(@g), "\n";
