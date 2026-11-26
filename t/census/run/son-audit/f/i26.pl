use v5.42;
my $x=1; my $r=\($x += 2); $$r *= 3; print "$x\n";
