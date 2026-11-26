use v5.42;
eval { eval { die "in\n" }; 1 } and print "ok[$@]\n";
