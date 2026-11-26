use v5.42;
my $n = 1; my $s = "abc"; $s =~ s/a/$n+1/e; print "$s\n";
