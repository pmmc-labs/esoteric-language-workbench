use v5.42;
my @a=(1,2); for my $x (@a) { eval { $x.="!"; die "x\n" } } print "@a\n";
