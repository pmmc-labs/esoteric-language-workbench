# kind: fault
# What a catch gets may be a reference, and a reference is no string (D112).
use v5.42;
try { die [1]; } catch ($e) { say "caught ", ref($e); print "as text: " . $e; }
