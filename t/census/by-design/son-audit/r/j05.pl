use v5.42;
my $s="abc"; my $r=\substr($s,0,1); $$r="Q"; print "$s\n";
