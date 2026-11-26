use v5.42;
our @a=(1,2); { local @a=(9); print "@a"; } print "@a\n";
