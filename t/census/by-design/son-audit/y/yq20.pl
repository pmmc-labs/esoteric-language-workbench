use v5.42;
our $g=1; sub p { $g } sub t { local $g = 5 for 1; p() } print t(), p(), "\n";
