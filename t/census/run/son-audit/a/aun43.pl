use v5.42;
my @a=(1,2,3); my $x = shift(@a) . shift(@a); print "$x @a\n";
