# kind: refused
# perl hands f's second parameter 9: the default ran before it was copied (T149, D76).
use v5.42;
my @a = (1, 2);
sub bump() { $a[1] = 9; return 5; }
sub f($x //= bump(), $y = 0) { return $x . "," . $y; }
say f(undef, $a[1]);
