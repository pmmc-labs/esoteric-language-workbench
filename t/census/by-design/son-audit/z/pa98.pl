use v5.42;
my @a=(1,2); sub last1 { $_[-1]=9 } last1(@a); print "@a\n";
