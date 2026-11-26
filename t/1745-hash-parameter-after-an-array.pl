# kind: refused
# perl does not compile it: Multiple slurpy parameters not allowed.
use v5.42;
sub f(@r, %o) { return 1 }
