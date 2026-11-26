use v5.42;
my @a=(undef,2); for (@a) { $_ //= 5 } print "@a\n";
