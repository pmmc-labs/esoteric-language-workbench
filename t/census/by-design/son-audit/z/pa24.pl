use v5.42;
sub f { $_[0]++ } f(my $x = 5); print "$x\n";
