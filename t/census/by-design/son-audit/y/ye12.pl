use v5.42;
our $g=1; sub f { "@_" } print f($g, sub { $g++ }->()), "\n";
