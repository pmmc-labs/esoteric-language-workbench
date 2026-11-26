use v5.42;
sub f { my ($x) = @_; return $x . scalar(@_) } print f(7, 8), "\n";
