use v5.42;
my @a=(1,2); sub f { return @a } my @c=f(); push @a,3; print "@c\n";
