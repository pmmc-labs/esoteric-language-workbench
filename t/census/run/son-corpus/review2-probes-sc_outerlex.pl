use v5.42;
my $c = 0; sub inc { $c = $c + 1; return 0 } inc(); inc(); print "$c\n";
