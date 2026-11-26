use v5.42;
my $s = ""; foreach my $x (1, 2) { if ($x > 1) { $s = $s . "b" } $s = $s . "|" } print "$s\n";
