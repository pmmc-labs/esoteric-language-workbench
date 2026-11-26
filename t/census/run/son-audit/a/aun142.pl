use v5.42;
my @a = (1); my $g = sub { push @a, 2 }; my $n = @a; $g->(); print "$n ", scalar(@a), "\n";
