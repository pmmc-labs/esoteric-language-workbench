use v5.42;
my $s=" a "; for ($s) { s/^\s+//; s/\s+$// } print "[$s]\n";
