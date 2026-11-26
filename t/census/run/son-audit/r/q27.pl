use v5.42;
my @a=(1); my $r=\@a; my @l=($a[0], ($r->[0]=2), $a[0]); print "@l\n";
