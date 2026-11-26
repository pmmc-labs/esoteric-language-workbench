use v5.42;
my $s="aXb"; my @p=split /X/,$s; $p[0]="z"; print "$s @p\n";
