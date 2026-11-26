use v5.42;
eval { do { die "d\n" } while (0); }; print "[$@]\n";
