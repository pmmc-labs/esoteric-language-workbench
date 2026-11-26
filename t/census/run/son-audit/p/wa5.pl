use v5.42;
my @a = (1,2); for my $i (1..2) { @a = (@a, $i) } print "@a\n";
