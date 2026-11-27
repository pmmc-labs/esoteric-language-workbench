# kind: fault
# perl gives the address with its first letter small: D112's fault.
use v5.42;
my $r = [1]; say "before"; say lcfirst $r;
