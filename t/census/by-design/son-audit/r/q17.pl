use v5.42;
my @a=(1,2,3); my $c = grep { $_-- > 1 } @a; print "$c @a\n";
