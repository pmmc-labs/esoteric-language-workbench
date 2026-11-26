use v5.42;
my @a=(1,2,3); my $s=join(",", @a, $a[0]=9); print "$s\n";
