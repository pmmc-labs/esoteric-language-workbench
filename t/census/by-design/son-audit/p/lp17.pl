use v5.42;
my $i = 0; my $s = ""; { $s .= $i; $i++; redo if $i < 3 } print "$s\n";
