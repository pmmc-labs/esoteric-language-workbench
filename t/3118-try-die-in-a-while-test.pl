# kind: refused
# perl: the line of the last statement the block ran (T316).
use v5.42;
my $i = 0;
while ($i < 2 || die "w") { $i++; }
