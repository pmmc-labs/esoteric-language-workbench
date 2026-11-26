use v5.42;
my @a=(1,2); my @l=($a[0], $a[0]++, $a[0]); print "@l\n";
