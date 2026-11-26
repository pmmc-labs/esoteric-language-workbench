use v5.42;
my $x=1; sub f { @_=(5,6); "@_" } print f($x), "$x\n";
