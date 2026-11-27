# kind: fault
# perl formats the reference's address as a number: D112's fault.
use v5.42;
my $r = [1]; say "before"; say sprintf("%d", $r);
