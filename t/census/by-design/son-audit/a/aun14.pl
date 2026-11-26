use v5.42;
our $g = 1; sub w { $g = 5; 0 } print $g, w(), $g, "\n";
