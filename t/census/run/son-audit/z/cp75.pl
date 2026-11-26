use v5.42;
my @a=("a","b"); my @c=@a; s/a/z/ for @a; print "@c|@a\n";
