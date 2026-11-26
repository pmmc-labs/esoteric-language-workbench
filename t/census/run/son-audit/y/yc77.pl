use v5.42;
my $x=1; my $r=\$x; my $n = $x + $$r++; print "$n\n";
