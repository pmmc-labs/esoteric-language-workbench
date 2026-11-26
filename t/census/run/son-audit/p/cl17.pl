use v5.42;
my $x = 1; my $g = sub { $x }; { local $_ = 9; $x = $_ } print $g->(), "\n";
