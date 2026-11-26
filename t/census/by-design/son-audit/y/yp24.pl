use v5.42;
my $x=1; sub f { $_[0]=9; @_=(5,6); scalar @_ } print f($x), "$x\n";
