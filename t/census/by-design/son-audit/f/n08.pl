use v5.42;
my @a=(1,2); eval { $_++ for @a; die "x\n" }; print "@a\n";
