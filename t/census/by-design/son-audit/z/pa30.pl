use v5.42;
my $x=1; sub inc { $_[0]++ } inc(do { $x }); print "$x\n";
