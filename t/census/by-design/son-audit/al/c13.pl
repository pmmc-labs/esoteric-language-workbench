use v5.42;
our $x="a"; sub f { $x.="b"; my @l=@_; "@l" } print f($x, "z"),"\n";
