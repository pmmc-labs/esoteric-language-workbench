use v5.42;
my ($q,$r)=(7,2); ($q,$r)=(int($q/$r),$q%$r); print "$q $r\n";
