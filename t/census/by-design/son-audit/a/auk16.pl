use v5.42;
sub t { for my $x (1) { die "t\n" } "end" } print eval { t() } // "died", "\n";
