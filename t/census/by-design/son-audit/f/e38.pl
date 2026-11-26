use v5.42;
sub f { die "f\n" } sub g { eval { f() }; print "g:$@"; die "g\n" } eval { g() }; print "m:$@";
