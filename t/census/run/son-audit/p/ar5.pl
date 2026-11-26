use v5.42;
my $x = 1; my $r = \$x; sub f { $_[0] = 7 } f($$r); print "$x\n";
