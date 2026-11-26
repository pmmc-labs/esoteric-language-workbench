use v5.42;
our $g=1; sub f { $g++ } print $g, f(), $g, "\n";
