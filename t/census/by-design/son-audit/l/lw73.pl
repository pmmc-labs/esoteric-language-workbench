use v5.42;
my @a=(1,2); for my $e (@a) { $e .= "x"; if ($e eq "1x") { last } } print "@a\n";
