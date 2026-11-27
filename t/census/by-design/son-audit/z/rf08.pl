use v5.42;
my $x=1; my $r=\$x; my $y=$x; $$r=5; print "$x$y\n";
