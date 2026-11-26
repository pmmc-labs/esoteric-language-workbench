# kind: refused
# perl warns: "my" variable %o masks earlier declaration in same scope.
use v5.42;
sub f(%o) { my %o = (a => 1); return scalar(%o) }
say f();
