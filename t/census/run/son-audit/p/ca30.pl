use v5.42;
sub f { print "f"; return 1 } sub g { print "g"; return 2 } print f() + g(), "\n";
