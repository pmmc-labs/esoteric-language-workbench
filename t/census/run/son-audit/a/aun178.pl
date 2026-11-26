use v5.42;
my $x = 3; my $r = \$x; my $y = $x++ + $$r; print "$y $x\n";
