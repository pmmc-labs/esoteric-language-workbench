use v5.42;
my @a=("ab"); my @l = ($a[0], $a[0] =~ tr/a/z/); print "@l\n";
