# kind: fault
# An uncaught message past ASCII without use open: perl writes the byte E9
# (T307).
use v5.42;
say "before";
die "caf\x{e9}";
