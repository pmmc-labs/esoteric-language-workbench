use v5.42;
sub f { my $n = shift; if ($n > 1) { print "b" } return $n } my $c = 2; if ($c) { print f(5) } print "\n";
