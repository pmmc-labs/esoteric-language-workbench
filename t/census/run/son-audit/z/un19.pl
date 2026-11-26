use v5.42;
eval { local $@; eval { die "x\n" }; 1 }; print "[$@]\n";
