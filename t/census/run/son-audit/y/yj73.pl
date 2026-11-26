use v5.42;
my $r; { my $x = 5; $r = \$x; } my $y = 6; print "$$r\n";
