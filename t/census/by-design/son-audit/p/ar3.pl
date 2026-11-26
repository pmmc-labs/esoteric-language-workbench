use v5.42;
my %h; sub f { $_[0] = 5 } f($h{new}); print $h{new} // "u", "\n";
