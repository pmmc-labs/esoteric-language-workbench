use v5.42;
sub f { my ($a, $b) = @_; return $a + $b } print f(1, 2), " ", f(1.5, "2"), "\n";
