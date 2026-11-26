use v5.42;
our $g=1; sub f { "@_" } for (1..2) { print f($g, $g++) } print "\n";
