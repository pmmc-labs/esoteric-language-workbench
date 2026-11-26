use v5.42;
sub t { eval { return 5 }; 6 } print t(), "\n";
