use v5.42;
eval { my @a = grep { die "m\n" } 1; }; print "[$@]\n";
