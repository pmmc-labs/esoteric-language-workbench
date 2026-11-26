use v5.42;
my $x="a"; my $r=\$x; $x.="b"; print "$$r\n";
