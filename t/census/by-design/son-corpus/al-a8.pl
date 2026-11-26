use v5.42;
sub ld { "l" . ($_[0] // "n") } my $f = 2; print ld($f), "\n";
