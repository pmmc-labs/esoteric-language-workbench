use v5.42;
sub f { print "f"; [[1,2],[3,4]] } sub g { print "g"; 1 } my $n = f()->[g()][g()]; print " $n\n";
