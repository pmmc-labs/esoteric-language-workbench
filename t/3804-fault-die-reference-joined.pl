# kind: fault
# A reference among several values is made a string, its address to perl (D112).
use v5.42;
say "before";
my $r = [1];
try { die "x", $r; } catch ($e) { say "caught"; }
