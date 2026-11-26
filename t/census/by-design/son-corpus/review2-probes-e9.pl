use v5.42;
sub f { my $n = shift; my $i = 0; while ($i < $n) { print $i; $i++ } return $i } print " ", f(3), "\n";
