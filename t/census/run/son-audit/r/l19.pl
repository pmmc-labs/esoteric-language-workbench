use v5.42;
my ($a1,$b1)=(0,1); for (1..10) { ($a1,$b1)=($b1,$a1+$b1) } print "$a1\n";
