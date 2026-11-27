use v5.42;
my $x = 5; my ($p, $q) = (\$x, \$x); $$p = 6; print "$$q\n";
