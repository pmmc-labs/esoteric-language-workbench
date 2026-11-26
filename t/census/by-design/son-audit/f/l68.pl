use v5.42;
my $s="abc"; my $o=""; while (length $s) { $o.=chop $s; } print "$o [$s]\n";
