use v5.42;
my $x=1; my $e=\$x; my @l = ($x, $$e = 7); print "@l\n";
