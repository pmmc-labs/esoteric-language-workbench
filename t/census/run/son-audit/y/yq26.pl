use v5.42;
my @p = split /,/, ""; my $n = @p; my $c = scalar(my @q = split /,/, ""); my @r = split /,/, ",,,"; print "$n$c", scalar(@r), "\n";
