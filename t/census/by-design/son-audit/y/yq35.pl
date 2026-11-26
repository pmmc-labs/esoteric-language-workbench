use v5.42;
my $s="abc"; for (substr($s,0,1)) { $_ = "ZZ" } print "$s\n";
