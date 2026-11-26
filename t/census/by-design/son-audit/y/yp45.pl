use v5.42;
my $x=1; sub f { my ($p)=@_; for ($_[0]) { $_ = 9 } $p } print f($x), "$x\n";
