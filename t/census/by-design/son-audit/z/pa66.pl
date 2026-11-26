use v5.42;
my @a=(1,2); for my $x (@a) { map { $_++ } $x } print "@a\n";
