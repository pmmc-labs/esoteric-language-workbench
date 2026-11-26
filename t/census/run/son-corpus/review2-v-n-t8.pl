use v5.42;
sub f { my $n = shift; return $n > 1 ? print("F") : 5 }
my $r = f(3); print "[", $r, "]\n";
