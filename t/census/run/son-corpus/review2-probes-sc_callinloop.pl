use v5.42;
sub f { my $n = shift; if ($n % 2) { print "o" } else { print "e" } return $n } for my $i (1..4) { f($i) } print "\n";
