use v5.42;
sub f { my $n = shift; if ($n) { print "t" } return 0 } f(1) for 1..2; print "\n";
