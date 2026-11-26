use v5.42;
sub f { my ($a, $b) = @_; return "$a-$b" } print f(1, "x"), f(2.5, 3), "\n";
