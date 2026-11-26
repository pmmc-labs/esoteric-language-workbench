use v5.42;
sub f { use warnings FATAL => "uninitialized"; my $x; return "a" . $x } print eval { f() } // "died", "\n";
