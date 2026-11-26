use v5.42;
my $s = ""; for my $n (0, 1) { my $r = eval { $s .= "a"; my $q = 1 / $n; $s .= "b"; $q }; $s .= defined $r ? "+" : "-" } print "$s\n";
