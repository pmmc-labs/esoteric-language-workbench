use v5.42;
eval { die "a\n" }; eval { die $@ . "b\n" }; print $@;
