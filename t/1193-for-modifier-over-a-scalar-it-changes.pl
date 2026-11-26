# kind: refused
# D77 for the modifier: its statement is its block.
use v5.42;
my $p = 1;
$p += $_ for $p, 2;
say $p;
