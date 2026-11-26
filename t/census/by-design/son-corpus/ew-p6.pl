use v5.42;
sub f { $main::c = $main::c + 1 } f(); f(); print "$main::c\n";
