use v5.42;
my @a=(1,2); for (@a) { $_ .= "x"; last } print "@a\n";
