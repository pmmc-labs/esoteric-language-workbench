# kind: fault
# perl takes the address for the position: D112's fault.
use v5.42;
my $r = [1]; say "before"; say rindex("abc", "b", $r);
