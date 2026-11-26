use v5.42;
my $c = 1; my $s = 5; my $t = 6; my @r = map { $_ *= 2 } ($c ? ($s, $t) : ()); print "@r $s $t\n";
