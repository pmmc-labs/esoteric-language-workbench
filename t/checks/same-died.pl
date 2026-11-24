# check: fails: perl wrote to stderr
# It dies, so it is a dies test, and this says same.
use v5.42;
say "before";
die "stopped\n";
