use v5.42;
our %g = (a=>1); my $n = keys %g; $g{b} = 2; print $n, scalar(keys %g), "\n";
