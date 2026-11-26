use v5.42;
sub f { my $n = shift; if ($n > 1) { print "b" } return $n } print f(2) + f(3), "\n";
