use v5.42;
my @a=(1,2); sub f { my $n=@_; push @a, 3; "$n@_" } print f(@a), "\n";
