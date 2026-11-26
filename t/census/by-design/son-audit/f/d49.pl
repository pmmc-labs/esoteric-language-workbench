use v5.42;
our $g=1; my $v = eval { local $g=2; $g*10 }; print "$v $g\n";
