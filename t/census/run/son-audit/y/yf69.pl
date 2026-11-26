use v5.42;
my $x=1; for my $i (1..3) { $x = $i == 2 ? [$i] : $i } print ref($x) ? "r" : $x, "\n";
