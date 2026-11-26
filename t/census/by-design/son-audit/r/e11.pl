use v5.42;
my @a=(1,2,3); my @b = grep { $_-- > 1 } @a; print "@a|@b\n";
