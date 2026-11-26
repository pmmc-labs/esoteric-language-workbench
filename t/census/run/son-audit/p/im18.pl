use v5.42;
my $x; { local $@; eval { die "in\n" }; $x = $@ } print "$x";
