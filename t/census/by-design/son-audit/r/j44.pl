use v5.42;
my @a=(1,2); my @l=(@a, push(@a,3), @a); print "@l\n";
