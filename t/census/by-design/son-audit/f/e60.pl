use v5.42;
eval { eval { die "in\n" }; }; print "[$@]\n";
