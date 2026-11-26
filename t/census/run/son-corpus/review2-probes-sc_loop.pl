use v5.42;
sub f { my $n = shift; for my $i (1 .. $n) { print $i } print "\n"; return 0 } f(2); f(3);
