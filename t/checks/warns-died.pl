# check: fails: an uncaught die
# kind: warns
# It dies: a dies test.
use v5.42;
warn "w\n";
die "x\n";
