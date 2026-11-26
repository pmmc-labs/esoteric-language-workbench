use v5.42;
my %h; sub f { print "f"; 0 } sub g { print "g"; 1 } $h{f()} .= g(); print "\n";
