use v5.42;
my $x = 1; my $g = sub { $x }; ($x, my $y) = (7, 8); print $g->(), " $y\n";
