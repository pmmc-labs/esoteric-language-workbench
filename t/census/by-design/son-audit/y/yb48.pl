use v5.42;
my @a=(1,2); for my $x (@a) { for my $y (@a) { $y++ } print $x } print " @a\n";
