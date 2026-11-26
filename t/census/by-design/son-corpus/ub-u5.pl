use v5.42;
sub f { my ($a, $b) = @_; return $a eq $b ? "e" : "n" } print f("a", "a"), f(1, "1.0"), "\n";
