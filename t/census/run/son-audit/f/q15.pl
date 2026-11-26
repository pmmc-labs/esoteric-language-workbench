use v5.42;
my $s="abab"; my @p; while ($s=~/b/g) { push @p, pos($s) } print "@p\n";
