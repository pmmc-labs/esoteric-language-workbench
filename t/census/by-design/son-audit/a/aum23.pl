use v5.42;
our $g = 1; sub t { local $g = 2; 1 } t(); print "$g\n";
