use v5.42;
sub f { return join("-", sort @_) } print f("c", "a", "b"), "\n";
