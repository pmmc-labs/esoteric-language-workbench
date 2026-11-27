# kind: fault
# A fault in a catch.
use v5.42;
try { die "x\n" } catch ($e) { print $e; my $n = "abc" + 1 }
