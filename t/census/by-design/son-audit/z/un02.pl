use v5.42;
our $g=1; eval { eval { local $g=2; die "a\n" }; print $g; local $g=3; die "b\n" }; print "$g $@";
