# kind: fault
# A whole Num from 10^15 in a message is D36's fault: perl prints 1e+15.
use v5.42;
say "before";
try { die 1e15 } catch ($e) { print $e }
