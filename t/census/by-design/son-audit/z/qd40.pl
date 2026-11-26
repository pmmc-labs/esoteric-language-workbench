use v5.42;
our $g=1; sub f { "@_" } my $s=f($g, $g++); print "$s $g\n";
