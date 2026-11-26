use v5.42;
sub f { my ($a) = @_; return $a ? "t" : "f" } print f(0), f("x"), f(""), "\n";
