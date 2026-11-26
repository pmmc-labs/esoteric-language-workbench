# kind: refused
# perl prints 2.
use v5.42;
my @a = (1, 2, 3);
sub f($n) { return $n; }
say "$a[f(1)]";
