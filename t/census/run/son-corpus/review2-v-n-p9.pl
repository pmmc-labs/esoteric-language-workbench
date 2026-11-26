use v5.42;
sub f { my $n = shift; unless ($n) { print "z" } }
my $r = f(0); print "[", $r, "]\n";
