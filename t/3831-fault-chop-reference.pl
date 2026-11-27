# kind: fault
# perl makes the address a string and chops it: D112's fault.
use v5.42;
my $r = [1]; say "before"; chop $r; say "after";
