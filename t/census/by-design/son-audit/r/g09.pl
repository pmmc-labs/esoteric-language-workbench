use v5.42;
our $g=1; sub f { $g=5; 1 } sub show { "@_" } print show($g, f(), $g), "\n";
