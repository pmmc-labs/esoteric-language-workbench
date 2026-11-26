use v5.42;
our $g = 1; sub f { $g = $g + 1 } f(); f(); print "$g\n";
