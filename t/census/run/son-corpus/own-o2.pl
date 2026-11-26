use v5.42;
my @a = (5, 6); my $n = 1; $n = $n + 0; if ($n) { $a[1] = $a[0] + 1 } print "@a\n";
