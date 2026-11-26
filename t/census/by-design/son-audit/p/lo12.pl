use v5.42;
our ($a1, $b1) = (1, 2); { local ($a1, $b1) = ($b1, $a1); print "$a1$b1" } print "$a1$b1\n";
