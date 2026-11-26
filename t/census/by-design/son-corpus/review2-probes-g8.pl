use v5.42;
sub f { my $n = shift; unless ($n) { print "x" } return 0 } f(0); f(1); print "\n";
