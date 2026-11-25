# kind: refused
# perl takes what follows last for an expression that names a label,
# and dies as it runs: Label not found for "last 1" (T120).
use v5.42;
my $i = 0;
while ($i++ < 3) {
    last + 1;
}
