# kind: refused
# perl does not compile it: catch block requires a (VAR) (T53).
use v5.42;
try { die "x\n" } catch { say "c"; }
