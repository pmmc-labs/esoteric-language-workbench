use v5.42;
sub f { my $n = shift; my $y = $n; if ($n) { $y = 9 } return $y }
print f(1), "\n";
