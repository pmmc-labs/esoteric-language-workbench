use v5.42;
our @a=(1,2,3); { local @a=(9); print "@a\n" } print "@a\n";
