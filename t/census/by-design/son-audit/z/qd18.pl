use v5.42;
sub ap { $_[0].="!" } my $x="a"; ap($x = "q"); print "$x\n";
