use v5.42;
my @a=(1); my $f=sub { push @a, 2 }; $f->(); my @b=@a; $f->(); print scalar(@b), scalar(@a), "\n";
