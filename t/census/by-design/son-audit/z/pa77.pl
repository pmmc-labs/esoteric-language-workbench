use v5.42;
our $g=1; sub f { $_[0]++; $g } print f($g),"\n";
