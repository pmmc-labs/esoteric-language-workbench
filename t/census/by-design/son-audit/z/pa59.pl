use v5.42;
my @a=(1,2,3); for my $x (@a) { $x*=10; last if $x==20 } print "@a\n";
