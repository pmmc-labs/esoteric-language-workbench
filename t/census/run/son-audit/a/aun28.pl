use v5.42;
my ($a,$b); my $r = \$a; (($a,$b) = (3,4)); print "$$r $b\n";
