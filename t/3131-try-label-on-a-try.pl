# kind: refused
# perl takes it; a label is on a loop (D61).
use v5.42;
L: try { die "x\n" } catch ($e) { say 1; }
