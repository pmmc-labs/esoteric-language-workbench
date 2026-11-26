use v5.42;
my $s="abc\n"; sub f { chomp $_[0] } f($s); print "[$s]\n";
