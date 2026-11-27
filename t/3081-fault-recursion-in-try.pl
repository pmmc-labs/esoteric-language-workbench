# kind: fault
# recursion too deep is a fault, and not caught (D13, D68): perl goes the
# 5000 calls down.
use v5.42;
no warnings 'recursion';
sub down($n) { return 0 if $n == 5000; return down($n + 1) + 1 }
say "before";
try { say down(0) } catch ($e) { print "caught\n" }
