use v5.42;
our $x = 1; my $s = ""; for my $i (1..2) { $s .= $x; $x = $x + 1 } print "$s $x\n";
