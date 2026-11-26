use v5.42;
our $x=1; sub d { $x=5; die "a\n" } eval { d() }; print "$x\n";
