use v5.42;
eval { my @a = map { die "m\n" } 1; }; print "[$@]\n";
