use v5.42;
my @a=(1,2); for my $x (@a) { my @t = map { $_++ } @a; print $x } print "\n";
