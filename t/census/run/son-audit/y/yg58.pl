use v5.42;
my $s="a\n\n"; my $n = chomp($s); my $t="abc"; my $c = chop($t); print length($s), "$n$c$t\n";
