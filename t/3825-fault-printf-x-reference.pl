# kind: fault
# perl prints the address in hex: D112's fault.
use v5.42;
my $r = {}; say "before"; printf("%x\n", $r);
