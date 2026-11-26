use v5.42;
our $g=1; sub h { $_[0] } sub f { "@_" } print f(h($g), $g++), "\n";
