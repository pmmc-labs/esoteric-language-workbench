use v5.42;
my $c = 1; if ($c) { sub f { my $n = shift; if ($n) { print "x" } return 1 } f(1) } print "\n";
