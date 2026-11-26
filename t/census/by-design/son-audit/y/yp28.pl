use v5.42;
my $x=1; sub f { push @_, 7; "@_" } print f($x), "\n";
