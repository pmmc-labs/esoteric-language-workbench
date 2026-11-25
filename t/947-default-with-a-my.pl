# kind: refused
# perl prints 3: a default may declare a variable.
use v5.42;
sub f($x = my $y = 3) { return $x; }
say f();
