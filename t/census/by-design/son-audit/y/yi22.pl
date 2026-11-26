use v5.42;
sub inc { $_[0]++ } my @a=(1,2); inc(shift @a); print "@a\n";
