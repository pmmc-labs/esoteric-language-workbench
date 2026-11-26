use v5.42;
my @a=(1,2); my @b; for my $x (@a) { push @b, \$x } ${$b[0]}=9; print "@a\n";
