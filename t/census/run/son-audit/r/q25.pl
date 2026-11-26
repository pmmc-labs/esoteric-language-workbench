use v5.42;
my $x=1; my $r=\$x; my $v = $x + ($$r=5); print "$v\n";
