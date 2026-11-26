use v5.42;
my $x=1; sub f { $_[0]=9; $_[1] } print f($x,$x), "\n";
