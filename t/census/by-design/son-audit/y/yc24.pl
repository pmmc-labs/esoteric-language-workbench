use v5.42;
sub inc { $_[0]++ } my $x=1; inc(++$x); print "$x\n";
