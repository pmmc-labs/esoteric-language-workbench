use v5.42;
my @a=(1,2); for (@a) { ($_,my $t)=($_*2,0) } print "@a\n";
