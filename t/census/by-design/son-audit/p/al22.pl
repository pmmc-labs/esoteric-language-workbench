use v5.42;
my @a = ([1],[2]); my @b = @a; $b[0][0] = 9; print "$a[0][0]\n";
