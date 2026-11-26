use v5.42;
my $s=""; $s .= $_ for grep { $_ % 2 } 1..5; print "$s\n";
