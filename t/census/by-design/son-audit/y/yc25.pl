use v5.42;
sub inc { $_[0]++ } my @a=(1); inc($a[0] = 5); print "@a\n";
