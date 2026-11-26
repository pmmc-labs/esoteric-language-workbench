use v5.42;
eval { die "x\n" }; eval { 1 }; print "[",$@,"]\n";
