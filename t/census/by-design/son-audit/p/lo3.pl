use v5.42;
our $g = 1; for my $i (1..2) { local $g = $g + $i; last if $i == 2 } print "$g\n";
