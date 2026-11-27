use v5.42;
my $x = 1; my $r = \$x; $$r = 3; print "$x\n";
