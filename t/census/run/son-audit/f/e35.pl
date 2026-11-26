use v5.42;
eval { die "a\n" }; { local $@; eval { die "b\n" }; } print $@;
