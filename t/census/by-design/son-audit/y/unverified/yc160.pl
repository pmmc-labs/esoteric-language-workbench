use v5.42;
my @a=(1,2,3); sub f { return (@a, $a[0]=9) } my @b=f(); print "@b\n";
