use v5.42;
my $n=0; my $z=0; sub cnt { $n++; 1 } my $r = eval { 1/$z + cnt() }; print "$n\n";
