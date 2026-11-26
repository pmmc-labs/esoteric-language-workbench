use v5.42;
my $k; sub g { $k // "u" } print g(), "\n"; $k = 3; print g(), "\n";
