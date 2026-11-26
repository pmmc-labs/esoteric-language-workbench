use v5.42;
my @a=(1,2); my @c=@a; undef @a; print "@c|", scalar(@a), "\n";
