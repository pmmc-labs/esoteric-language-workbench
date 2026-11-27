# kind: fault
# A reference interpolated into qq is its address to perl: D112's fault.
use v5.42;
my $r = [1];
say "before";
say qq{$r};
