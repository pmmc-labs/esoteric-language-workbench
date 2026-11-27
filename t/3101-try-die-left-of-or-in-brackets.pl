# kind: refused
# perl is silent here, and dies x; refused all the same (D146).
use v5.42;
my $x = (die "x") || 1;
