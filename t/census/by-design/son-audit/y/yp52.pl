use v5.42;
my $x=1; sub f { my $r=\$_[0]; $$r=9; return } f($x); print "$x\n";
