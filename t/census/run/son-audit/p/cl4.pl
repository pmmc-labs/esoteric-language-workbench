use v5.42;
my $x = 1; my $g = sub { $x }; $x++; $x .= "a"; print $g->(), "\n";
