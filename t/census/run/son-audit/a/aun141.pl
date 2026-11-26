use v5.42;
my $x = 1; my $g = sub { $x++ }; my $a = $x; $g->(); my $b = $x; print "$a $b\n";
