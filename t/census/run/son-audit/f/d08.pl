use v5.42;
sub f { local $@="keep"; eval { die "x\n" }; } eval { die "outer\n" }; f(); print $@;
