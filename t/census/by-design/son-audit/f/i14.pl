use v5.42;
my $x=1; sub inc { $_[0]++ } inc($x += 1); print "$x\n";
