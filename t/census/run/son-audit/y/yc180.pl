use v5.42;
my @a=(1,2); my $s = "@a" . ($a[0]=9) . "@a"; print "$s\n";
