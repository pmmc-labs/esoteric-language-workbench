use v5.42;
eval { die "a\n" }; my $e=$@; eval { die "b\n" }; print "$e$@";
