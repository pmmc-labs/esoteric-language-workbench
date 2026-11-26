use v5.42;
our $g=1; sub f { local $g=2; die "x\n" } eval { f() }; print "$g $@";
