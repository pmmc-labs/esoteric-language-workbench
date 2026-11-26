use v5.42;
our $g = 1; sub f { $g = 5; 0 } print $g + f(), "\n";
