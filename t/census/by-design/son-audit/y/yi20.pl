use v5.42;
sub inc { $_[0]++ } my @a=(1,2); inc($_) for @a; print "@a\n";
