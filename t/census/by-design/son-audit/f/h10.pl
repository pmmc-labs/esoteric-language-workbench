use v5.42;
our $x=1; sub f { $x=2; shift } print f($x),"\n";
