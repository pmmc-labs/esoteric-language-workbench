# kind: fault
# A fault is not caught by try (D13, T306): perl runs the catch.
use v5.42;
say "before";
try { my $x = 1 / 0 } catch ($e) { print "caught: $e" }
say "after";
