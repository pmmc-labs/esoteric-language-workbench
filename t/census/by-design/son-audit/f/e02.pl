use v5.42;
sub f { eval { return 1 }; return 2 } print f(),"\n";
