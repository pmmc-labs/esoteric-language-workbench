# kind: fault
# say STDERR of a wide character without use open: perl warns (T307).
use v5.42;
warn "said\n";
say STDERR "\x{263a}";
