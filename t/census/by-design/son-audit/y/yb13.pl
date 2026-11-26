use v5.42;
my @a=(1,2); for my $x (map { $_ } @a) { $x++ } print "@a\n";
