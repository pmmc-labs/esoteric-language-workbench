use v5.42;
our $g=1; sub f { $_[0] = "w"; "@_" } print f($g, $g++), " $g\n";
