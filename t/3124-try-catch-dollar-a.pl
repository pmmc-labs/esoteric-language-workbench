# kind: refused
# perl takes it; $a is the sort's (D55).
use v5.42;
try { die "x\n" } catch ($a) { say "c"; }
