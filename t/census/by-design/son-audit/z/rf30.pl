use v5.42;
my $x=1; my $r=\$x; for (1..3) { $$r+=$x } print "$x\n";
