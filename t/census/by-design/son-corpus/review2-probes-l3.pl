use v5.42;
sub f { my $n = shift; if ($n > 5) { exit 3 } return 1 } f(1); print "ok\n";
