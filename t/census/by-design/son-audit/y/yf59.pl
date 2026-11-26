use v5.42;
my @a=(1,2,3); for my $x (@a) { last if $x == 2; $x *= 10 } print "@a\n";
