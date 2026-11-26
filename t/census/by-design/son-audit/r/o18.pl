use v5.42;
sub g { $_="g" } my @a=(1,2); for (@a) { g() } print "@a\n";
