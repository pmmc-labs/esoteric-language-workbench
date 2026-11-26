use v5.42;
my ($p,$q)=(1,1); ($p, $q) = ($q, $p+$q) for 1..5; print "$p $q\n";
