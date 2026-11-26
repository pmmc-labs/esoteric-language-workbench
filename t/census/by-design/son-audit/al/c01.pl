use v5.42;
my $x=1; sub f { $x=2; $_[0] } print f($x),"\n";
