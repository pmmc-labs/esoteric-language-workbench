use v5.42;
my $x=1; my $r=\$x; for ($$r) { $_=7 } print "$x\n";
