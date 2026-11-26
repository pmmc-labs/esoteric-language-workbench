use v5.42;
our ($x,$y)=(1,2); *y=\$x; $y=7; print "$x\n";
