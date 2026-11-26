use v5.42;
my $z=0; my $s="a"; eval { $s .= "b"; $s .= 1/$z; $s .= "c" }; print "$s\n";
