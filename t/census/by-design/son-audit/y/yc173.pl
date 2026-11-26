use v5.42;
our @a=(1,2); my @b=(@a, $a[0]=9); print "@b\n";
