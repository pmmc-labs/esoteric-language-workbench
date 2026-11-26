use v5.42;
my @a=("ab","c"); my @l = (@a, $a[0] =~ tr/a/z/); print "@l\n";
