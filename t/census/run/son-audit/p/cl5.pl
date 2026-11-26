use v5.42;
my $x = 1; my $g = sub { $x }; for my $i (1..3) { $x += $i } print $g->(), "\n";
