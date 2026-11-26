use v5.42;
our $g = "a"; sub f { $g = "b"; "" } print $g . f(), "\n";
