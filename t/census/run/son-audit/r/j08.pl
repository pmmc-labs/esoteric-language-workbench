use v5.42;
my $s="a,b,c"; my @p=split /,/, $s; $s="z"; print "@p $s\n";
