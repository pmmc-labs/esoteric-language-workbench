use v5.42;
my @a=(1,2,3); my @b=(@a, do { $_++ for @a; 0 }); print "@b\n";
