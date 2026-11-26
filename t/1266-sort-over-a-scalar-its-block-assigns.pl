# kind: refused
# perl: 01 (D77).
use v5.42;
my $p = 3;
my $q = 1;
my @r = sort { $p = 0; $a <=> $b } ($p, $q);
say @r;
