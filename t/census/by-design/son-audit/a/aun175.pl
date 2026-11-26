use v5.42;
my $s = "x"; my $t = ($s .= "y") . ($s .= "z"); print "$t $s\n";
