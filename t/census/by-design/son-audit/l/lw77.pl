use v5.42;
my @a=(1,2); for (@a) { last if $_ eq "2"; $_ .= "x" } print "@a\n";
