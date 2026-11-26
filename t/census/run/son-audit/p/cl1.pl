use v5.42;
my $x = 1; my $g = sub { $x }; ($x) = (7); print $g->(), "\n";
