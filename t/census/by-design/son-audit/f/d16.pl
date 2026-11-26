use v5.42;
our $g=1; sub d { die "x\n" } sub f { local $g=2; my $s="a".d()."b"; $s } eval { f() }; print "$g\n";
