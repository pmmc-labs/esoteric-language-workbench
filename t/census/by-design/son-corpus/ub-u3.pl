use v5.42;
sub f { my ($a) = @_; return defined($a) ? "d" : "u" } print f(1), f(undef), "\n";
