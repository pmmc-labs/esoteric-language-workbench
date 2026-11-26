use v5.42;
my $x=1; sub f { my ($p)=@_; ($_[0], my $t) = (9, 1); $p } print f($x), "$x\n";
