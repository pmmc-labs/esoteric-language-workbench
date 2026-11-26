use v5.42;
my ($x, $y) = (1, 2); my $g = sub { "$x$y" }; ($x, $y) = ($y, $x); print $g->(), "\n";
