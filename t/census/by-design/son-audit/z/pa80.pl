use v5.42;
my $s="abc"; sub f { $_[0]=~s/b/X/ } f($s); print "$s\n";
