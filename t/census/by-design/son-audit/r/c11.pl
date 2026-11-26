use v5.42;
our $g=1; sub f { local $g=2; my $z=shift; 1/$z } sub k { f(0) } eval { k() }; print "$g\n";
