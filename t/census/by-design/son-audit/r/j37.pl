use v5.42;
my $x=5; sub show { "@_" } print show($x, $x++, $x), "\n";
