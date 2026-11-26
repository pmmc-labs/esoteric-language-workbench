use v5.42;
my $x="a"; $_ .= "!" for ($x .= "b"); print "$x\n";
