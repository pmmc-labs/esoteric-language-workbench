use v5.42;
my $x=1; my $r=\$x; print $x, ($$r=2), "\n";
