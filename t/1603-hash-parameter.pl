# kind: refused
# perl: 1. Step 12b.
use v5.42;
sub f(%o) { return scalar(%o) }
say f(a => 1);
