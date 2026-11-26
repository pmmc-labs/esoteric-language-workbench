use v5.42;
our $g = "a"; sub f { return $g } $g = 2.5; print f(), "\n";
