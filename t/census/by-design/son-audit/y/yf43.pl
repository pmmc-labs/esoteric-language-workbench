use v5.42;
my @a=(undef,2); for my $x (@a) { $x //= 5 } print "@a\n";
