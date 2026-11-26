use v5.42;
our $n; BEGIN { $n = 1 } BEGIN { $n++ } $n++; print "$n\n";
