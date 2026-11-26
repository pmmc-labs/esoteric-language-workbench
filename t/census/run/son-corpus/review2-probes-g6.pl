use v5.42;
sub f { my $n = shift; print "a" if $n; return 1 } f(1); f(0); print "\n";
