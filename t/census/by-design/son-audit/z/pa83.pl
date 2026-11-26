use v5.42;
my $x=1; sub f { my $v=shift; $v++; $v } print f($x),$x,"\n";
