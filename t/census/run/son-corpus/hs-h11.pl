use v5.42;
my $n = 1; my $r = \$n; $$r = $$r + 4; print "$n\n";
