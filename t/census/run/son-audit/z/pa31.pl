use v5.42;
my $x=1; my $r=\$x; sub inc { $_[0]++ } inc($$r); print "$x\n";
