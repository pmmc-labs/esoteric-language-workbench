use v5.42;
my $s=""; for my $i (1..4) { eval { die "e$i\n" if $i%2; $s.="ok$i " }; $s.=$@ if $@; } print $s;
