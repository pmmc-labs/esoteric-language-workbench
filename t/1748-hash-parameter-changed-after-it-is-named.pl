# kind: refused
# perl: 5.
use v5.42;
sub f(%o) { my @l = (%o, delete $o{a}); return scalar(@l) }
say f(a => 1, b => 2);
