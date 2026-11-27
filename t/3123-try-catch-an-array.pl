# kind: refused
# perl does not compile it: syntax error.
use v5.42;
try { die "x\n" } catch (@e) { say "c"; }
