use v5.42;
our $g="a"; sub f { "@_" } print f($g, $g .= "b"), "\n";
