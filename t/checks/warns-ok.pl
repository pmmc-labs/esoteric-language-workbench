# check: ok
# kind: warns
# A program that warns and ends: stdout, then stderr (D149).
use v5.42;
say "a";
warn "w\n";
warn "where";
say "b";
