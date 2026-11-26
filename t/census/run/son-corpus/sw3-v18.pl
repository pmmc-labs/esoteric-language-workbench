use v5.42;
my $h = { list => [1, 2] }; push @{ $h->{list} }, 3; print scalar(@{ $h->{list} }), "\n";
