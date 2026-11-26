use v5.42;
my $str = ""; for my $i (1 .. 3) { $str .= $i; $str .= "," unless $i == 3 } print "$str\n";
