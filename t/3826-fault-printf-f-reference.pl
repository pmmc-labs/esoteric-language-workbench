# kind: fault
# perl prints the address as a float: D112's fault.
use v5.42;
my $r = [1]; say "before"; printf("%5.2f\n", $r);
