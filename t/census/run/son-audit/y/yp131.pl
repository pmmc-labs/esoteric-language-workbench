use v5.42;
my $x="a"; my @t = grep { s/a/z/ } ($x .= "a"); print "$x\n";
