use v5.42;
eval { for my $x (1) { die "m\n" } }; print "[$@]\n";
