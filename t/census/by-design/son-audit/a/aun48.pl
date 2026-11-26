use v5.42;
my @a=(1,2,3); my $l = splice(@a,0,1) + @a; print "$l\n";
