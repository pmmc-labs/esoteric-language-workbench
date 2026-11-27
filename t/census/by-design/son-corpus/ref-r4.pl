use v5.42;
my $n = 5; my $sr = \$n; print $$sr, "\n"; $$sr = 6; print "$n\n";
