# kind: refused
# perl: 72; the map walks $p itself (D77, T180).
use v5.42;
my $p = 1;
my $q = 2;
my @r = map { $p = 7; $_ } ($p, $q);
say @r;
