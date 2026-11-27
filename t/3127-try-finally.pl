# kind: refused
# perl warns: try/catch/finally is experimental (T313, D144).
use v5.42;
try { die "x\n" } catch ($e) { say "c"; } finally { say "f"; }
