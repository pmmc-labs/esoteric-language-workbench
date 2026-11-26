use v5.42;
my $x="a"; s/a/z/ for ($x .= "a"); print "$x\n";
