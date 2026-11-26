use v5.42;
my @a=(1,2,3); sub f { @_=(); } f(@a); print "@a\n";
