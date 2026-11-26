use v5.42;
my @a=(1,2); for my $x (@a) { $_++ for @a; print $x } print " @a\n";
