use v5.42;
our $g=1; { local $g=2; eval { local $g=3; }; print "$g\n" } print "$g\n";
