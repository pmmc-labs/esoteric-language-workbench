use v5.42;
my $x=1; sub f { my $p=$_[0]; $_[0]=9; $p } print f($x), "\n";
