use v5.42;
my $x=1; my @l=($x, do { $x=7 }); print "@l\n";
