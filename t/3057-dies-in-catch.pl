# kind: dies
# A die in a catch, with no try round it.
use v5.42;
try { die "first\n" } catch ($e) { die "again: $e" }
