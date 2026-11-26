use v5.42;
my $x=1; sub f { "@_" } print f($x = 2, $x = 3), "\n";
