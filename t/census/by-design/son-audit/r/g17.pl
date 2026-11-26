use v5.42;
our $g=1; sub f { $g=5; 1 } my ($p,$q,$r)=($g, f(), $g); print "$p$q$r\n";
