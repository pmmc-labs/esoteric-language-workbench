use v5.42;
my $c=0; my $f = sub { $c++; die "x\n" }; eval { $f->() }; eval { $f->() }; print "$c\n";
