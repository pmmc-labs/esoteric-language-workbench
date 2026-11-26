use v5.42;
my @a=(1,2,3); my @b=(scalar(@a), push(@a,9), scalar(@a)); print "@b\n";
