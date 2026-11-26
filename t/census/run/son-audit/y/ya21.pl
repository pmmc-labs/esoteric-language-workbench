use v5.42;
my %h=(k=>1); sub f { my ($p)=@_; $h{k}=9; $p } print f($h{k}), "\n";
