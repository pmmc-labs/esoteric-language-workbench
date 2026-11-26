use v5.42;
our $g=1; our $h=1; sub f { "@_" } print f($g, $h++, $g++, $h), "\n";
