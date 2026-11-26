use v5.42;
my @a=(1,2); my $s=""; sub w { $a[0] = "q" } for my $x (@a) { $x .= "y"; w(); $s .= $x } print "$s|@a\n";
