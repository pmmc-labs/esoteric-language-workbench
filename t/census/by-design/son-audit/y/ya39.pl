use v5.42;
my $x=1; sub f { my ($p)=@_; $_++ for @_; "$p@_" } print f($x), "$x\n";
