# kind: dies
# A die caught, and a later one not.
use v5.42;
try { die "one\n" } catch ($e) { print "caught $e" }
for my $i (1 .. 3) { die "in the loop at $i" if $i == 2; say $i }
