use v5.42;
my ($a,$b,$c)=(1,2,3); ($a,$b,$c)=($c,$a); print $a,$b,defined $c?1:0,"\n";
