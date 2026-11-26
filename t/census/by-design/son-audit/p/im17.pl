use v5.42;
$_ = "x"; sub f { $_ = "y" } f(); print "$_\n";
