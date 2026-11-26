use v5.42;
our $g=1; sub f { local $g=2; my $z=shift; 5 % $z } eval { f(0) }; print "$g\n";
