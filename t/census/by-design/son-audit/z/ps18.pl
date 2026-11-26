use v5.42;
my @a=(0,2); for (@a) { $_ ||= 5 } print "@a\n";
