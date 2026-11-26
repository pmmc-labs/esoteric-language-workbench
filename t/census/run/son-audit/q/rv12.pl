use v5.42;
my @x; push @x, 1; my @c = @x; push @x, 2; print "@c|@x\n";
