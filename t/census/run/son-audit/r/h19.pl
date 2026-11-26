use v5.42;
my @a=(1,2,3); my ($f,@r)=splice(@a,0,2); print "$f|@r|@a\n";
