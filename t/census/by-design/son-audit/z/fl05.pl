use v5.42;
my @a=(1,2,3); my @b=(@a, map { $_++ } @a); print "@b\n";
