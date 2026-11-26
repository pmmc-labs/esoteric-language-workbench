use v5.42;
my $x=1; my $r=\$x; my @l=($x, ($$r=2), $x); print "@l\n";
