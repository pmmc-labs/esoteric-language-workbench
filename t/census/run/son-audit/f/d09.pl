use v5.42;
sub f { local $,="-"; die "x\n" } eval { f() }; print 1,2,"\n";
