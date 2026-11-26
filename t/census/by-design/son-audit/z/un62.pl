use v5.42;
our $g=1; sub f { local $g=2; eval { die "in\n" }; die "out\n" } eval { f() }; print "$g $@";
