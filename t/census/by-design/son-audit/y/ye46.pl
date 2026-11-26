use v5.42;
our $g=1; sub f { my ($p,$q)=@_; "$p $q" } print f($g, $g++), "\n";
