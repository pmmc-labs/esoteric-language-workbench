use v5.42;
our $g=1; sub f { local $g=2; my $o; $o->foo } eval { f() }; print "$g ", ($@?1:0), "\n";
