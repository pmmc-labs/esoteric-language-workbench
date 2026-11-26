use v5.42;
my $s = "abc"; if ($s =~ /(b)/) { my $p = $1; "xyz" =~ /(y)/; print "$p $1\n"; }
