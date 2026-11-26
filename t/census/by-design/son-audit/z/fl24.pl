use v5.42;
my @a=(1,2); my @b=($#a, pop @a, $#a); print "@b\n";
