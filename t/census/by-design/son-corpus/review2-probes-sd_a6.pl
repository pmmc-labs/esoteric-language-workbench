use v5.42;
sub f { my $n = shift; if ($n > 1) { print "b" } return $n } print f(f(2)), "\n";
