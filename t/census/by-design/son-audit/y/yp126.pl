use v5.42;
my $x="a"; my @t = map { $_ .= "!" } ($x .= "b"); print "$x\n";
