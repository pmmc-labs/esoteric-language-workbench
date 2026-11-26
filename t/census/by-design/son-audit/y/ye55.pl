use v5.42;
our $g=1; sub f { "@_" } my $v = $g; print f($v, $g++), "\n";
