use v5.42;
sub f { eval { return 5 }; 7 } print f(), "\n";
