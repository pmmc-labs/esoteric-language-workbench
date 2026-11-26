use v5.42;
our $g=1; eval { local $g = 2; my $o; $o->foo; }; print "$g\n";
