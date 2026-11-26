use v5.42;
sub f { my ($x) = @_; return $x > 2 ? "big" : "small" } print f($_), " " for 1 .. 4; print "\n";
