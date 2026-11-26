use v5.42;
my %h; sub f { 1 } f($h{new}); print exists $h{new} ? "viv" : "none", "\n";
