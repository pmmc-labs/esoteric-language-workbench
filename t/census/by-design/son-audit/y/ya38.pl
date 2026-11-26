use v5.42;
my $x=1; sub f { my ($p)=@_; for (@_) { $_++ } $p } print f($x), "$x\n";
