# check: ok
# kind: warns
# And its exit status, when that is not 0.
use v5.42;
warn "w\n";
exit 3;
