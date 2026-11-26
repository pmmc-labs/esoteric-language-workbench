use v5.42;
our ($x,$y)=(1,2); s/^/a/ for $x,$y; print "$x $y\n";
