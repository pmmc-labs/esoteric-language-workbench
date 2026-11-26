use v5.42;
my @a; sub f { print "f"; 0 } sub g { print "g"; 1 } $a[f()] = g(); print "\n";
