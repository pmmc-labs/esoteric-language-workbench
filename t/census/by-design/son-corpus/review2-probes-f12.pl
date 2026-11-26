use v5.42;
sub f { my $n = shift; my @a = (1,2); if ($n) { push @a, 3 } return scalar(@a) } print f(1), f(0), "\n";
