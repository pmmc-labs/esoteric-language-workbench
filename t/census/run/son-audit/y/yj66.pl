use v5.42;
sub f { "f1" } BEGIN { *g = \&f } print g(), "\n";
