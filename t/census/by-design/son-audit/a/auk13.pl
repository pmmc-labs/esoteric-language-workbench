use v5.42;
eval { die "a\n" for 1; }; print "[$@]\n";
