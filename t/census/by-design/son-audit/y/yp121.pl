use v5.42;
my $x="a"; for my $v ($x .= "b") { $v .= "!" } print "$x\n";
