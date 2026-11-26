use v5.42;
sub f { local $_ = "in"; die "x\n" } $_="out"; eval { f() }; print "$_\n";
