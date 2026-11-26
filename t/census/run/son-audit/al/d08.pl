use v5.42;
my ($p,$q,$r)=(1,2,3); my $c=0; ($c ? $p : $c ? $q : $r) = 9; print "$p$q$r\n";
