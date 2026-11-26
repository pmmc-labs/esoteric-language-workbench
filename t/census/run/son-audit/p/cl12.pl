use v5.42;
my $x = 1; my $g = sub { $x }; $x = $x + 1 while $x < 5; print $g->(), "\n";
