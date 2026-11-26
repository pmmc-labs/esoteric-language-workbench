use v5.42;
my $x=1; sub f { my ($p)=@_; $x++; my ($q)=@_; $x++; my $r=shift; "$p$q$r" } print f($x), "\n";
