use v5.42;
our @a=(1); for ($a[0], $a[2]) { $_ //= 7 } print "@a\n";
