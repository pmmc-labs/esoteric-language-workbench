use v5.42;
sub f { my $n = shift; while ($n > 0) { print $n; $n = $n - 1 } return 0 } f(3); print "\n";
