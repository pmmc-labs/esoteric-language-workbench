use v5.42;
my @a=(1,2,3); $_++ for grep { $_ > 1 } @a; print "@a\n";
