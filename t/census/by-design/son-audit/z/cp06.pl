use v5.42;
my @a=(1,2); my @c=@a; my @t=map { $_++ } @a; print "@c|@a\n";
