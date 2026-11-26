use v5.42;
my $r=[1,2]; sub inc { $_[0]++ } inc($r->[0]); print "@$r\n";
