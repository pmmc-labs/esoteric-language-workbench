use v5.42;
sub f { my $n = shift; if ($n > 1) { print "b" } return 0 } foreach my $i (1, 2, 3) { f($i); print "|" } print "\n";
