use v5.42;
our $g=1; sub t { local $g = 2; for my $i (1..3) { local $g = $g + $i; return $g if $i == 2 } 0 } print t(), $g, "\n";
