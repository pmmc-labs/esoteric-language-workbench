use v5.42;
my @a=(1,2); sub f { my ($p,$q)=@_; $_[0]=9; "$p$q" } print f(@a),"@a\n";
