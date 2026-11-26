use v5.42;
my @a=(1,2); my @c=@a; $_*=2 for @a; print "@c|@a\n";
