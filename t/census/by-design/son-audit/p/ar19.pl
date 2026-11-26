use v5.42;
sub f { chomp $_[0] } my $s = "x\n"; f($s); print "[$s]\n";
