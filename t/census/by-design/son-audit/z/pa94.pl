use v5.42;
my $x=1; sub f { ($_[0],my $t)=(8,9); $t } print f($x),$x,"\n";
