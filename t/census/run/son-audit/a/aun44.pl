use v5.42;
my $s = "abc"; my $n = ($s =~ s/b/x/) + ($s =~ s/x/y/); print "$n $s\n";
