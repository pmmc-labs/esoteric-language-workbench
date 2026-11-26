use v5.42;
our $g=1; my $m="m"; sub m { shift; "@_" } print main->$m($g, $g++), "\n";
