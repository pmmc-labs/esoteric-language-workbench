use v5.42;
our $g=1; sub f { local $g=2; 1 } eval { f(); die "x\n" }; print "$g\n";
