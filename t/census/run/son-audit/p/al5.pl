use v5.42;
my $x = 1; my @l = map { $_ * 2 } $x; $x = 3; print "@l $x\n";
