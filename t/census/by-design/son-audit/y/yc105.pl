use v5.42;
sub f { print "f"; 5 } sub g { print "g"; 2 } my $n = f() - g() * f(); print " $n\n";
