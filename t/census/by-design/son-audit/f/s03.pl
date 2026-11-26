use v5.42;
our $x=1; { local $x=$x+1; print $x; } print "$x\n";
