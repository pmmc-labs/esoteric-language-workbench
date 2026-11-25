# kind: refused
# perl does not compile it: a $ alone is a parameter, in a signature, and nothing anywhere else.
use v5.42;
sub f($, $y) { return $y; }
say f($, 2);
