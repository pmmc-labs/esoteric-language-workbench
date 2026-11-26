use v5.42;
eval { die "a\n" }; eval { 1 }; print "[$@]\n";
