use v5.42;
our $g = 1; sub dbl { $g *= 2 } my $i = 0; do { $g = $g + 1; dbl(); $i++ } until $i >= 2; print "$g\n";
