# check: ok
# kind: dies
# An uncaught die: perl's stdout, then its stderr, then exit: 255 (D12).
use v5.42;
say "before";
die "stopped\n";
