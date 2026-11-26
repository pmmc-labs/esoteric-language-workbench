use v5.42;
my $s=""; for my $i (1..3) { eval { next if $i==2; $s.=$i; }; } print "$s\n";
