use v5.42;
my $x = 1; my $g = sub { $x }; my $y; $y = $x = 8; print $g->(), "$y\n";
