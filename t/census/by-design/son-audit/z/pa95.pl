use v5.42;
my $x="a"; sub f { $_[0].="b"; $_[0].="c" } f($x); print "$x\n";
