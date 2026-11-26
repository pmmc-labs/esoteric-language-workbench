use v5.42;
my ($a1,$b1)=("p","q"); my $c=1; ($c ? $a1 : $b1) .= "x"; print "$a1$b1\n";
