use v5.42;
our $x=0; { $x++; redo if $x<3; } print "$x\n";
