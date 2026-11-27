use v5.42;
my @a=(1,2); for my $x (@a) { my $r=\$x; $$r++ } print "@a\n";
