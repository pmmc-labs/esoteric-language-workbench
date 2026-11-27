# kind: refused
# perl takes it; there is no empty statement.
use v5.42;
try { die "x\n" } catch ($e) { say 1; };
