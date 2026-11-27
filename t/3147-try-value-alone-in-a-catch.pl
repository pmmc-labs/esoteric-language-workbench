# kind: refused
# perl warns: Useless use of a constant in void context.
use v5.42;
try { die "x\n" } catch ($e) { "c"; }
