use v5.42;
my @w = (3, 4); my $s = ""; while (my $n = shift @w) { $s .= "[$n]" } print "$s\n";
