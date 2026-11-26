use v5.42;
eval { for my $x (1,2) { print "p$x\n"; die "m\n" } }; print "[$@]\n";
