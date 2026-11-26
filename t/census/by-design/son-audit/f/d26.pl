use v5.42;
my $v = eval { die "x\n"; 1 } || "dead"; print "$v\n";
