use v5.42;
my @a=(1,2,3); for my $x (map { $_ } @a) { $x=0 } print "@a\n";
