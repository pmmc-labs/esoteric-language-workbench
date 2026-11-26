use v5.42;
my $x = 5; sub f { my $n = shift; if ($n) { $x = 7 } return $n } f(1); print "$x\n";
