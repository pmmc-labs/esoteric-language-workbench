# kind: fault
# A warn past ASCII without use open: perl writes the byte E9 (T307).
use v5.42;
say "before";
warn "caf\x{e9}\n";
