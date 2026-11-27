# kind: refused
# perl is silent here, and dies; refused all the same (D146).
use v5.42;
until (die "x\n") { say 1; }
