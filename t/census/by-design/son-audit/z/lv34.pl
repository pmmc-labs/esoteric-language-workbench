use v5.42;
sub inc { $_[0]++ } my $x="a"; inc($x .= "b"); print "$x\n";
