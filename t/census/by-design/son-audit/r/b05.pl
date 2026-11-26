use v5.42;
our @a=(1); eval { local @a=(2,3); die "x\n" }; print "@a\n";
