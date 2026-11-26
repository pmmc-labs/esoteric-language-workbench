use v5.42;
sub f { my ($a, $b) = @_; return $a == $b ? "e" : "n" } print f(1, "1.0"), f(2, 3), "\n";
